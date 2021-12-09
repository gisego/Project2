import requests
from bs4 import BeautifulSoup



# Etape 1
# Ecrire une fonction category(base_url) qui retourne les liens des categories dans un dictionnaire. Ex: return {"travel": 'http://books.toscrape.com/travel......'}

def category():
    base_url = 'http://books.toscrape.com'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    uls = soup.find('ul', class_= 'nav nav-list')
    all_a = uls.find_all('a')
    for hrefs in all_a:
        my_dictio = {}
        category_name = hrefs.text
        category_name = category_name.replace('\n', '')
        category_name = category_name.replace(' ', '')
        href = hrefs['href']
        hrefs = base_url + '/' + href
        my_dictio[category_name] = hrefs

    return my_dictio

print(category())


# Etape
# 2
#
# Ecrire
# une
# fonction
# pages_livre(url_category)
# qui
# prend
# en
# parametre
# l
# 'url d'
# une
# categorie
#
# Et
# qui
# retourne
# l
# 'url de tous les livres de cette categorie sous forme de list.
#
# Ex:
# return [http: // books.toscrape.com / travel / .... /, http: // books.toscrape.com / travel / .... /]
#
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