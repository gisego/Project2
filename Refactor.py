import requests
from bs4 import BeautifulSoup

#Obtenir les pages de toute la categorie
def get_all_categories_pages(category):
    list_sa = []
    i = 0
    while True:
        i = i + 1
        if i == 1:
            url_general = "http://books.toscrape.com/catalogue/category/books/" + category + "/index.html"
            list_sa.append(url_general)
        else:
            url_general = "http://books.toscrape.com/catalogue/category/books/" + category + "/page-" + str(i) + ".html"  # concatenar
            page_general = requests.get(url_general)
            if page_general.status_code != 200:
                break
            list_sa.append(url_general)
    return list_sa

def find_categories_names():
    url = 'http://books.toscrape.com/catalogue/category/books_1/index.html'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    list_categories = []
    ultags = soup.find("ul", class_= "nav nav-list")
    for litags in ultags.find_all("a"):
        links_categories = litags['href']
        if links_categories.startswith(".."):
            links_categories = links_categories.replace('../books/', '')
            for links_categoriess in links_categories:
                links_categoriess = links_categories.replace('/index.html', '')
            list_categories.append(links_categoriess)
    return list_categories

def all_links_products_from_categories():
    list_links_products = []
    for url in get_all_categories_pages(category):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        for all_links in soup.find_all("div", class_= "image_container"):
            for all_as in all_links.find_all("a"):
                for links in all_as:
                    links = all_as['href']
                    links_clean = "http://books.toscrape.com/catalogue/" + links
                    links_finished = links_clean.split('../../../')
                    links_last = ''.join(links_finished)
                    # print(links_last)
                list_links_products.append(links_last)
    return list_links_products

def product_page_url():
    product_Page_Url_list = []
    for url in all_links_products_from_categories():
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        product_Page_Url = r.url
        product_Page_Url_list.append(product_Page_Url)
    return product_Page_Url_list

def title():
    title_list = []
    for url in all_links_products_from_categories():
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        title = soup.find("title").getText()
        title_list.append(title)
    return title_list

def image():
    image_url_list = []
    for url in all_links_products_from_categories():
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        image_Url = soup.find("img")["src"]
        for image_url_clean in image_Url:
            image_url_clean = "http://books.toscrape.com" + image_Url #recomponer el url
            for image_Url_last in image_url_clean:
                image_Url_last = image_url_clean.split('../..')
                for image_all_url in image_Url_last:
                    image_all_url = ''.join(image_Url_last)
        image_url_list.append(image_all_url)
    return image_url_list

def product_description():
    product_description_list = []
    for url in all_links_products_from_categories():
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        product_Description = soup.find("p", class_="")
        product_description_list.append(product_Description)
    return product_description_list

def product_category():
    category_list = []
    for url in all_links_products_from_categories():
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        ultag = soup.find("ul", class_="breadcrumb")
        category = ultag.find_all("li")[2].text
        category_list.append(category)
    return category_list

def universal_product_code():
    universal_code_list = []
    for url in all_links_products_from_categories():
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        tds = soup.find_all("td")
        universal_Product_Code = tds[0].text
        universal_code_list.append(universal_Product_Code)
    return universal_code_list

def price_excluding_tax():
    price_excluding_tax_list = []
    for url in all_links_products_from_categories():
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        tds = soup.find_all("td")
        price_Excluding_Tax = tds[2].text
        price_excluding_tax_list.append(price_Excluding_Tax)
    return price_excluding_tax_list

def price_including_tax():
    price_including_tax_list = []
    for url in all_links_products_from_categories():
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        tds = soup.find_all("td")
        price_Including_Tax = tds[3].text
        price_including_tax_list.append(price_Including_Tax)
    return price_including_tax_list

def number_available():
    number_available_list = []
    for url in all_links_products_from_categories():
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        tds = soup.find_all("td")
        number_Available = tds[5].text
        number_available_list.append(number_Available)
    return number_available_list

def review_rating():
    review_rating_list = []
    for url in all_links_products_from_categories():
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        tds = soup.find_all("td")
        review_Rating = tds[6].text
        review_rating_list.append(review_Rating)
    return review_rating_list

# creation du fichier csv

import csv
#
en_tete = ["product_page_url", "title", "image_all_url", "product_description", "category", "universal_product_code",
               "price_excluding_tax", "price_including_tax", "number_available", "review_rating"]


for category in find_categories_names():
    filename = category + ".csv"
    with open(filename, 'w') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(en_tete)

for category in find_categories_names():
    product_info = all_links_products_from_categories()
    for ligne in product_info:
        ligne = product_page_url(), title(), image(), product_description(), product_category(), universal_product_code(), price_excluding_tax(), price_including_tax(), number_available(), review_rating()
        with open(filename, 'w') as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=',')
            writer.writerow(ligne)

# # Data from all products
# list_data_products = {
#      "product_Page_Url_list": [],
#     "title_list" : [],
# image_url_list = []
# product_description_list = []
# category_list = []
# universal_code_list = []
# price_excluding_tax_list = []
# price_including_tax_list = []
# number_available_list = []
# review_Rating_list = []
#}