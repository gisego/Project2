import requests
from bs4 import BeautifulSoup
# from pathlib import Path
# import wget
# import csv


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


def page_livre(url_category):
    liens_livres = []
    r = requests.get(url_category)
    soup = BeautifulSoup(r.content, 'html.parser')
    nom_page = soup.find('li', class_='current')
    categories = str(url_category.replace('/index.html', ''))
    if r.ok:
        if nom_page is not None:
            nom_page = (soup.find('li', class_='current').text).replace(' ','')[9]
            for nom_page in range(int(nom_page)):
                url = categories+'/page-' + str(nom_page+1) + '.html'
                re = requests.get(url)
                soup1 = BeautifulSoup(re.content, 'html.parser')
                if re.ok:
                    for liens in soup1.find_all("div", class_= "image_container"):
                        for allas in liens.find_all('a'):
                            lien = allas['href'].replace('../../../', 'http://books.toscrape.com/catalogue/')
                        liens_livres.append(lien)
        else:
            for links in soup.find_all("div", class_="image_container"):
                for alls in links.find_all('a'):
                    liens = alls['href'].replace('../../../', 'http://books.toscrape.com/catalogue/')
                liens_livres.append(liens)
    return liens_livres




print(page_livre('http://books.toscrape.com/catalogue/category/books/travel_2/index.html'))
#
# # for category in find_categories_names():
# #     pages = get_pagination(category)
# #     for url_category in pages:
# #         page_product = page_livre(url_category)
#
#
#
# # Etape 3  Ecrire fonction Write_image(lien_image_livre, nom_categorie)# qui utilise path et wget pour classer en fonction des parametres "lien_image_livre, nom_categorie"
#
# def download_image(image_url, category):
#     base_image = 'images'
#     path = f'{base_image}/{category}'
#     Path(path).mkdir(parents=True, exist_ok=True)
#     wget.download(image_url, path, bar=None)
#
# def info_from_category(liens):
#     infos = []
#     for link in liens:
#         # print("Le lien livre ===============>", link)
#         livre_info = livre(link)
#         # print("Le livre ===============>", livre_info)
#         infos.append(livre_info)
#         # print("La description ===============>", infos)
#         download_image(livre_info['image_url'], livre_info['category'])
#     return infos
#
#
# # download_image('http://books.toscrape.com/media/cache/6d/41/6d418a73cc7d4ecfd75ca11d854041db.jpg', 'travel')
#
# # Etape 4 Ecrire # une fonction livre(lien_un_livre) qui recupere les infos du livre et appelle la fonction write_image(lien_image_livre, nom_categorie) et retourne les infos du livre dans un dictionnaire.
#
#
# def livre(lien_un_livre):
#     dictio = {}
#     r = requests.get(lien_un_livre)
#     soup = BeautifulSoup(r.content, 'html.parser')
#     product_page_url = r.url
#     dictio['Product_page'] = product_page_url
#     titre = soup.find("title").getText()
#     titre = titre.replace('\n', '')
#     titre = ''.join(titre)
#     dictio['Title'] = titre
#     image_Url = soup.find("img")["src"]
#     image_Url = "http://books.toscrape.com" + image_Url
#     image_Url = image_Url.split('../..')
#     image_Url = ''.join(image_Url)
#     dictio['Image_url'] = image_Url
#     product_Description = soup.find("p", class_="")
#     dictio['Description'] = product_Description
#     ultag = soup.find("ul", class_="breadcrumb")
#     category = ultag.find_all("li")[2].text
#     category= category.replace('\n', '')
#     dictio['Categorie'] = category
#     tds = soup.find_all("td")
#     universal_Product_Code = tds[0].text
#     dictio['Universal_code'] = universal_Product_Code
#     price_Excluding_Tax = tds[2].text
#     dictio['Price_excluding_tax'] = price_Excluding_Tax
#     price_Including_Tax = tds[3].text
#     dictio['Price_including_tax'] = price_Including_Tax
#     number_Available = tds[5].text
#     dictio['number_available'] = number_Available
#     review_Rating = tds[6].text
#     dictio['review_Rating'] = review_Rating
#     return dictio
#
# # # Etape 5 Ecrire une fonction write_csv(infos_livre, nom categorie) qui ouvre un fichier csv avec pour nom la categorie passé en parametre, puis enregistre les infos "infos_livre" recu dans
# # # le csv.
#
# titres =['product_page_url',
#             'universal_product_code',
#             'title',
#             'price_including_tax',
#             'price_excluding_tax',
#             'number_available',
#             'product_description',
#             'category',
#             'review_rating',
#             'image_url']
# def write_csv(info_livre, nom_categorie):
#     file_csv = nom_categorie + '.csv'
#     with open(file_csv, 'w', newline='', encoding='iso-8859-1') as fichier_csv:
#         ### my adds
#         write = csv.DictWriter(fichier_csv, fieldnames=titres)
#         write.writeheader()
#         # writer = csv.writer(fichier_csv, delimiter=',')
#         # for info_livr in info_livre:
#         write.writerow({'product_page_url': info_livre['lien'],
#                              'universal_product_code': info_livre['universal_product_code'],
#                              'title': info_livre['Title'],
#                              'price_including_tax': info_livre['price_including_tax'].strip(),
#                              'price_excluding_tax': info_livre['price_excluding_tax'].strip(),
#                              'number_available': info_livre['number_available'].strip(),
#                              'product_description': str(info_livre['product_description']),
#                              'category': info_livre['category'].strip(),
#                              'review_rating': info_livre['review_rating'].strip(),
#                              'image_url': info_livre['image_url']})
#
# #### Exemple TEST
# info_livre = {"lien": 'testurl', "universal_product_code": 'UPC', "Title": 'titre', "price_including_tax": 'price_in',
#          "price_excluding_tax": 'price_ex', "number_available": 'available', "product_description": 'descrip',
#          "category": 'cat', "review_rating": 'rating', "image_url": 'image'}
# nom_categorie = "Cat"
# print(write_csv(info_livre, nom_categorie))
#
# # Etape 6 Organiser toutes les fonctions dans le main du fichier.
# if __name__ == '__main__':
#     categories = category()
#     for category in categories.keys():
#         links = get_pagination(categories[category])
#         print(links)
#
#
