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

def page_livre():
    url = 'http://books.toscrape.com/catalogue/category/books_1/index.html'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    list_categories = []
    ultags = soup.find("ul", class_= "nav nav-list")
    for litags in ultags.find_all("a"):
        links_categories = litags['href']
        if links_categories.startswith(".."):
            links_categories = links_categories.replace('../books/', '')
            links_categories = links_categories.replace('/index.html', '')
            list_categories.append(links_categories)

            for category in list_categories:
                list_sa = []
                i = 0
                while True:
                    i = i + 1
                    if i == 1:
                        url_general = "http://books.toscrape.com/catalogue/category/books/" + category + "/index.html"
                        list_sa.append(url_general)
                    else:
                        url_general = "http://books.toscrape.com/catalogue/category/books/" + category + "/page-" + str(
                            i) + ".html"
                        page_general = requests.get(url_general)
                        if page_general.status_code != 200:
                            break
                        list_sa.append(url_general)

                        for url in list_sa:
                            list_links_products = []
                            r = requests.get(url)
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

print(page_livre())












#
#
# Etape
# 3
#
# Ecrire
# fonction
# Write_image(lien_image_livre, nom_categorie)
# qui
# utilise
# path
# et
# wget
# pour
# classer
#
# en
# fonction
# des
# parametres
# "lien_image_livre, nom_categorie"
#
# Etape
# 4
#
# Ecrire
# une
# fonction
# livre(lien_un_livre)
# qui
# recupere
# les
# infos
# du
# livre
# et
# appelle
# la
# fonction
#
# write_image(lien_image_livre, nom_categorie)
# et
# retourne
# les
# infos
# du
# livre
# dans
# un
# dictionnaire.
#
# Etape
# 5
#
# Ecrire
# une
# fonction
# write_csv(infos_livre, nom
# categorie) qui
# ouvre
# un
# fichier
# csv
# avec
# pour
# nom
#
# la
# categorie
# passé
# en
# parametre, puis
# enregistre
# les
# infos
# "infos_livre"
# recu
# dans
# le
# csv.
#
# Etape
# 6
#
# Organiser
# toutes
# les
# fonctions
# dans
# le
# main
# du
# fichier.