import requests
from bs4 import BeautifulSoup
url = "http://books.toscrape.com/catalogue/birdsong-a-story-in-pictures_975/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


#url_Product_Page
product_Page_Url = page.url
if product_Page_Url == page.url:
    print(page.url)


#title
for title in soup.find("title"):
    print(title.text)


#image's Url
image_Url = soup.find("img")
if image_Url == soup.find("img"):
    print(image_Url["src"])

#Product's description
for product_Description in soup.find("p", class_=""):
    print(product_Description.text)

#category
ultag = soup.find("ul", class_= "breadcrumb")
category = ultag.find_all("li")[2].getText()
print(category)

#Universal Product Code
tds = soup.find_all("td")
for universal_Product_Code in tds[0]:
    print(universal_Product_Code)

#Price Excluding Tax
for price_Excluding_Tax in tds[2]:
    print(price_Excluding_Tax)

#Price_Including_Tax
for price_Including_Tax in tds[3]:
    print(price_Including_Tax)

#Number_Available
for number_Available in tds[5]:
    print(number_Available)

#review_Rating
for review_Rating in tds[6]:
    print(review_Rating)
#Création de la liste
en_tete = ["product_Page_Url", "title", "image_Url", "product_Description", "category", "universal_Product_Code", "price_Excluding_Tax", "price_Including_Tax", "number_Available", "review_Rating"]

#creation du fichier csv
import csv
doctos = open('Project2.csv', 'w')
writer = csv.writer(doctos, delimiter=',')
writer.writerow(en_tete)

#export des infos

writer.writerow([product_Page_Url, title, image_Url, product_Description, category, universal_Product_Code, price_Excluding_Tax, price_Including_Tax, number_Available, review_Rating])






