# User selects a product and the link goes here
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen


# my_url = 'https://www.goodguide.com/products/420447-garnier-color-shield-shampoo-reviews-ratings#/'

def page_soup(my_url):
    req = Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})

    web_byte = urlopen(req).read()
    page_html = web_byte.decode('utf-8')

    # html parsing
    return soup(page_html, 'lxml')

page_soup = page_soup(my_url)

# get rating
def get_rating():
    for thing in page_soup.find_all("p", {"class": "ring-value number"}):
        return thing.text.strip()


# get ingredients
def get_ingredients():
    ingredients = []
    for lists in page_soup.find_all("ul", {"class": "list product-details-ingredients"}):
        for a in lists.find_all('a'):
            ingredients.append(a.text)
    return ingredients


# get links
def get_ingred_links():
    links = []
    for lists in page_soup.find_all("ul", {"class": "list product-details-ingredients"}):
        for a in lists.find_all('a'):
            link = a.get('href')
            links.append(link)
    url = 'https://www.goodguide.com'
    complete_links = []
    for link in links:
        complete_links.append(url + link)
    return complete_links

# for one ingredient
def ingred_hazard(get_ingred_link, get_ingredient):
    page_soup(get_ingred_link)
    # to get description
    for item in page_soup.find_all("div", {"class": "large-offset-3 large-6 columns"}):
        ul = item.descendants
        for thing in ul:
            try:
                for li in thing.find_all("li"):
                    descrip_dict[get_ingredient] = li.text.strip()
            except:
                continue

def the_ingred_loop():
    i = 0
    get_ingredients = get_ingredients()
    get_ingred_links = get_ingred_links()
    for get_ingred_link in get_ingred_links:
        ingred_hazard(get_ingred_link, get_ingredients[i])
        i = i + 1



