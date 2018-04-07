from bs4 import BeautifulSoup
import requests

url = "https://www.amazon.in/gp/bestsellers/electronics/1389432031/ref=zg_bs_nav_e_2_3561110031"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
}

modelNameList, ratingList, numberOfRatingList, priceList = [], [], [], []
new_url_list = []


def find_child_nodes(parent_node, selector, soup_obj):
    try:
        return parent_node.select(selector)[0]

    except:
        # In case of no element found, create a dummy empty tag
        return soup_obj.new_tag('DIV')


def fetch_items(url):
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    center_list_wrapper = soup.select('#zg_centerListWrapper .zg_itemImmersion')

    for node in center_list_wrapper:
        modelNameList.append(find_child_nodes(node, '.a-section.a-spacing-none > a > div:nth-of-type(2)', soup))
        ratingList.append(find_child_nodes(node, '.a-icon-row.a-spacing-none > a:nth-of-type(1)', soup))
        numberOfRatingList.append(find_child_nodes(node, '.a-icon-row.a-spacing-none > a:nth-of-type(2)', soup))
        priceList.append(find_child_nodes(node, 'span.a-size-base.a-color-price > span', soup))


resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")
paginationList = soup.select('.zg_pagination .zg_page a')  # Pagination)

for pagination in paginationList:
    new_url = str(pagination['href'])
    new_url_list.append(new_url)

for url in new_url_list:
    fetch_items(url)

filename = "products.csv"

with open(filename, 'w') as f:
    headers = "Name, Price, Rating, Number_of_ratings \n"
    f.write(headers)

    for i in range(len(modelNameList)):
        name = modelNameList[i].text.strip().replace(',', ':')
        rating = ratingList[i].text.strip().replace(',', ':')
        numberOfRating = numberOfRatingList[i].text.strip().replace(',', '')
        price = priceList[i].text.strip().replace(',', '')
        f.write('{},{},{},{}\n'.format(name, price, rating, numberOfRating))