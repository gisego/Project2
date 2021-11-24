import requests
from bs4 import BeautifulSoup

#categories sans pagination


def url_category_simple(category):
    url_simple = []
    url_base = "http://books.toscrape.com/catalogue/category/books/" + category + "/index.html"
    url_simple.append(url_base)
    return url_simple

categorias = ['travel_2', 'classics_6', 'phylosophy_7', 'womens-fiction_9', 'religion_12', 'music_14', 'science-fiction_16', 'sports-and-games_17', 'new-adult_20', 'science_22', 'poetry_23', 'paranormal_24', 'art_25', 'psychology_26', 'autobiography_27', 'parenting_28', 'adult-fiction_29', 'humor_30', 'horror_31', 'history_32', 'christian-fiction_34', 'business_35', 'biography_36', 'thriller_37', 'contemporary_38', 'spirituality_39', 'academic_40', 'self-help_41', 'historical_42', 'christian_43', 'suspense_44', 'short-stories_45', 'novels_46', 'health_47', 'politics_48', 'cultural_49', 'erotica_50', 'crime_51']



# Trouver touts les produits de chaque category


list_links_products = []
for categoria in categorias:
    for url in url_category_simple(categoria):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        for all_links in soup.find_all("div", class_= "image_container"):
            for all_as in all_links.find_all("a"):
                for links in all_as:
                    links = all_as['href']
                    for links_clean in links:
                        links_clean = "http://books.toscrape.com/catalogue/" + links
                        for links_finished in links_clean:
                            links_finished = links_clean.split('../../../')
                            for links_last in links_finished:
                                links_last = ''.join(links_finished)
                    # print(links_last)
                    list_links_products.append(links_last)
#
# list_data_products = {}
product_Page_Url_list = []
title_list = []
image_url_list = []
product_description_list = []
category_list = []
universal_code_list = []
price_excluding_tax_list = []
price_including_tax_list = []
number_available_list = []
review_Rating_list = []

for url in list_links_products:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    #url_Product_Page
    product_Page_Url = r.url
    product_Page_Url_list.append(product_Page_Url)


    #title
    title = soup.find("title").getText()
    title_list.append(title)

    #image's Url
    image_Url = soup.find("img")["src"]
    for image_url_clean in image_Url:
        image_url_clean = "http://books.toscrape.com" + image_Url #recomponer el url
        for image_Url_last in image_url_clean:
            image_Url_last = image_url_clean.split('../..')
            for image_all_url in image_Url_last:
                image_all_url = ''.join(image_Url_last)
    image_url_list.append(image_all_url)



    # Product's description
    product_Description = soup.find("p", class_="")
    product_description_list.append(product_Description)


    # category
    ultag = soup.find("ul", class_="breadcrumb")
    category = ultag.find_all("li")[2].text
    category_list.append(category)

    # Universal Product Code
    tds = soup.find_all("td")
    universal_Product_Code = tds[0].text
    universal_code_list.append(universal_Product_Code)


    #Price Excluding Tax
    price_Excluding_Tax = tds[2].text
    price_excluding_tax_list.append(price_Excluding_Tax)


    # Price_Including_Tax
    price_Including_Tax = tds[3].text
    price_including_tax_list.append(price_Including_Tax)

    # Number_Available
    number_Available = tds[5].text
    number_available_list.append(number_Available)

    # review_Rating
    review_Rating = tds[6].text
    review_Rating_list.append(review_Rating)


print(review_Rating_list)


    #
    # #
    # # # # Création de la liste
    # en_tete = ["product_Page_Url", "title", "image_all_url", "product_Description", "category", "universal_Product_Code",
    #                "price_Excluding_Tax", "price_Including_Tax", "number_Available", "review_Rating"]
    #
    # # # creation du fichier csv
    # import csv
    #
    # with open('test4.csv', 'w') as fichier_csv:
    #     writer = csv.writer(fichier_csv, delimiter=',')
    #     writer.writerow(en_tete)
    # #
    # # # export des infos
    #     for product_Page_Url, title, image_all_url, product_Description, category, universal_Product_Code,price_Excluding_Tax, price_Including_Tax, number_Available, review_Rating in zip(product_Page_Url_list, title_list, image_url_list, product_description_list, category_list, universal_code_list, price_excluding_tax_list,
    #          price_including_tax_list, number_available_list, review_Rating_list):
    #         ligne = [product_Page_Url, title, image_all_url, product_Description, category, universal_Product_Code,price_Excluding_Tax, price_Including_Tax, number_Available, review_Rating]
    #
    #         writer.writerow(ligne)




