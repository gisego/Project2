import requests
from bs4 import BeautifulSoup



# Etape 1
# Ecrire une fonction category(base_url) qui retourne les liens des categories dans un dictionnaire. Ex: return {"travel": 'http://books.toscrape.com/travel......'}
#
def category():
    base_url = 'http://books.toscrape.com'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    uls = soup.find('ul', class_= 'nav nav-list')
    all_a = uls.find_all('a')
    my_dictio = {}
    for hrefs in all_a:
        category_name = hrefs.text
        category_name = category_name.replace('\n', '')
        category_name = category_name.replace(' ', '')
        href = hrefs['href']
        hrefs = base_url + '/' + href
        my_dictio[category_name] = hrefs
    my_dictio.pop('Books')
    return my_dictio

# Etape 2 Ecrire une fonction pages_livre(url_category) qui prend en parametre l'url d'une categorie Et qui retourne l'url de tous les livres de cette categorie sous forme de list.
# Ex: return [http: // books.toscrape.com / travel / .... /, http: // books.toscrape.com / travel / .... /]


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

def get_pagination(category):
    list_sa = []
    i = 0
    while True:
        i = i + 1
        if i == 1:
            url_general = "http://books.toscrape.com/catalogue/category/books/" + category + "/index.html"
            list_sa.append(url_general)
        else:
            url_general = "http://books.toscrape.com/catalogue/category/books/" + category + "/page-" + str(
                i) + ".html"  # concatenar
            page_general = requests.get(url_general)
            if page_general.status_code != 200:
                break
            list_sa.append(url_general)
    return list_sa

def page_livre(url_category):
    list_links_products = []
    r = requests.get(url_category)
    soup = BeautifulSoup(r.content, 'html.parser')
    for all_links in soup.find_all("div", class_="image_container"):
        for all_as in all_links.find_all("a"):
            for links in all_as:
                links = all_as['href']
                links_clean = "http://books.toscrape.com/catalogue/" + links
                links_finished = links_clean.split('../../../')
                links_last = ''.join(links_finished)
            list_links_products.append(links_last)
    return list_links_products


# for category in find_categories_names():
#     pages = get_pagination(category)
#     for url_category in pages:
#         page_product = page_livre(url_category)



# Etape 3  Ecrire fonction Write_image(lien_image_livre, nom_categorie)# qui utilise path et wget pour classer en fonction des parametres "lien_image_livre, nom_categorie"

# def write_image(lien_image_livre, nom_categorie):




# Etape 4 Ecrire # une fonction livre(lien_un_livre) qui recupere les infos du livre et appelle la fonction write_image(lien_image_livre, nom_categorie) et retourne les infos du livre dans un dictionnaire.


def livre(lien_un_livre):
    dictio = {}
    r = requests.get(lien_un_livre)
    soup = BeautifulSoup(r.content, 'html.parser')
    product_page_url = r.url
    dictio['Product_page'] = product_page_url
    titre = soup.find("title").getText()
    titre = titre.replace('\n', '')
    titre = ''.join(titre)
    dictio['Title'] = titre
    image_Url = soup.find("img")["src"]
    image_Url = "http://books.toscrape.com" + image_Url
    image_Url = image_Url.split('../..')
    image_Url = ''.join(image_Url)
    dictio['Image_url'] = image_Url
    product_Description = soup.find("p", class_="")
    dictio['Description'] = product_Description
    ultag = soup.find("ul", class_="breadcrumb")
    category = ultag.find_all("li")[2].text
    category= category.replace('\n', '')
    dictio['Categorie'] = category
    tds = soup.find_all("td")
    universal_Product_Code = tds[0].text
    dictio['Universal_code'] = universal_Product_Code
    price_Excluding_Tax = tds[2].text
    dictio['Price_excluding_tax'] = price_Excluding_Tax
    price_Including_Tax = tds[3].text
    dictio['Price_including_tax'] = price_Including_Tax
    number_Available = tds[5].text
    dictio['number_available'] = number_Available
    review_Rating = tds[6].text
    dictio['review_Rating'] = review_Rating
    return dictio

# Etape 5 Ecrire une fonction write_csv(infos_livre, nom categorie) qui ouvre un fichier csv avec pour nom la categorie passé en parametre, puis enregistre les infos "infos_livre" recu dans
# le csv.
import csv

def write_csv(info_livre, nom_categorie):
    file_csv = nom_categorie + '.csv'
    with open(file_csv, 'w') as fichier_csv:
     writer = csv.writer(fichier_csv, delimiter=',')
     writer.writerow(info_livre)

#### Exemple TEST
info_livre = {"lien": 'page_url', "universal_product_code": 'UPC', "Title": 'titre', "price_including_tax": 'price_in',
         "price_excluding_tax": 'price_ex', "number_available": 'available', "product_description": 'descrip',
         "category": 'cat', "review_rating": 'rating', "image_url": 'image'}
nom_categorie = "Cat"
print(write_csv(info_livre, nom_categorie))

# Etape 6 Organiser toutes les fonctions dans le main du fichier.