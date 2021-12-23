# -*- coding: utf-8 -*-
from typing import List, Any, Union

import requests
from bs4 import BeautifulSoup
import wget
from pathlib import Path
import pandas as pd
import csv


titres =['product_page_url',
            'universal_product_code',
            'title',
            'price_including_tax',
            'price_excluding_tax',
            'number_available',
            'product_description',
            'category',
            'review_rating',
            'image_url']
#Etape 1:
base_url = 'https://books.toscrape.com'
reponse = requests.get(base_url)

def category_links(base_url):
    if reponse.ok:
        liensCat = {}
        soup = BeautifulSoup(reponse.text, 'html.parser')
        for category in soup.find('ul', class_='nav nav-list').find('li').find('ul').find_all('li'):
            categories = category.a.get('href').replace('/index.html', '')
            # liensCat.append('https://books.toscrape.com/' + categories)
            titre = category.text.strip()
            liensCat[titre]='https://books.toscrape.com/' + categories
    return liensCat

# Etape 2
# categorie = "https://books.toscrape.com/catalogue/category/books/travel_2"
def pages_livre(categorie):
    reponse_cat = requests.get(categorie)
    if reponse_cat.ok:
        links = []
        soup = BeautifulSoup(reponse_cat.text, 'html.parser')
        number_of_pages = soup.find('li', attrs={'class': 'current'})
        if number_of_pages is not None:
            number_of_pages = int(number_of_pages.text.split('of ')[1])
            for npage in range(1, number_of_pages + 1):
                url_cat2 = categorie + "/page-" + str(npage) + '.html'
                reponse_cat2 = requests.get(url_cat2)
                soup = BeautifulSoup(reponse_cat2.text, 'html.parser')
                articles = soup.findAll('article')
                for article in articles:
                    a = article.find('a')
                    link = a['href'].replace('../../../', '')
                    links.append('https://books.toscrape.com/catalogue/' + link)
        else:
            articles = soup.findAll('article')
            for article in articles:
                a = article.find('a')
                link = a['href'].replace('../../../', '')
                links.append('https://books.toscrape.com/catalogue/' + link)
    return links

#Etape 3
#Ecrire fonction Write_image(lien_image_livre, nom_categorie) qui utilise path et wget pour classer
# en fonction des parametres "lien_image_livre, nom_categorie"
def download_image(image_url, category):
    base_image = 'images'
    path = f'{base_image}/{category}'
    Path(path).mkdir(parents=True, exist_ok=True)
    wget.download(image_url, path, bar=None)


def info_from_category(liens):
    infos = []
    for link in liens:
        # print("Le lien livre ===============>", link)
        livre_info = livre(link)
        # print("Le livre ===============>", livre_info)
        infos.append(livre_info)
        # print("La description ===============>", infos)
        download_image(livre_info['image_url'], livre_info['category']) 
    return infos

#Etape 4 
#Ecrire une fonction livre(lien_un_livre) qui recupere les infos du livre et appelle la fonction
#write_image(lien_image_livre, nom_categorie) et retourne les infos du livre dans un dictionnaire.

def livre(lien_un_livre):
    reponse_livre = requests.get(lien_un_livre)
    if reponse_livre.ok:
        soup = BeautifulSoup(reponse_livre.text, 'html.parser')
        page_url = lien_un_livre
        UPC = soup.find_all('td')[0].text
        titre = soup.find('h1').text
        price_in = soup.find_all('td')[3].text.replace('Â', '')
        price_ex = soup.find_all('td')[2].text.replace('Â', '')
        available = soup.find_all('td')[5].text.replace('In stock (', '').replace('available)', '')
        descrip = soup.find_all('p')[3].text
        cat = soup.find_all('a')[3].text
        rating = soup.find("p", attrs={'class': 'star-rating'}).get("class")[1]
        image = (soup.find('img')['src'].replace('../../', 'https://books.toscrape.com/'))

    return {"lien": page_url, "universal_product_code": UPC, "Title": titre, "price_including_tax": price_in,
         "price_excluding_tax": price_ex, "number_available": available, "product_description": descrip,
         "category": cat, "review_rating": rating, "image_url": image}
#attention sur la présentation le texte apparait avec encore des crochés à voir ou ça ne passe pas le .text
# plus ajout de l'étape 3 !!

#Etape 5
#Ecrire une fonction write_csv(infos_livre, nom categorie) qui ouvre un fichier csv avec pour nom
#la categorie passé en parametre, puis enregistre les infos "infos_livre" recu dans le csv.



def write_csv(infos_livre, category):
    with open(f'{category}.csv', 'w', newline='', encoding='iso-8859-1') as file:
        write = csv.DictWriter(file, fieldnames=titres)
        write.writeheader()
        
        for infos_livr in infos_livre:
                write.writerow({'product_page_url': infos_livr['lien'],
                             'universal_product_code': infos_livr['universal_product_code'],
                             'title': infos_livr['Title'],
                             'price_including_tax': infos_livr['price_including_tax'].strip(),
                             'price_excluding_tax': infos_livr['price_excluding_tax'].strip(),
                             'number_available': infos_livr['number_available'].strip(),
                             'product_description': str(infos_livr['product_description']),
                             'category': infos_livr['category'].strip(),
                             'review_rating': infos_livr['review_rating'].strip(),
                             'image_url': infos_livr['image_url']})


#Etape 6
#Organiser toutes les fonctions dans le main du fichier.
if __name__ == '__main__':
    ## 
    categories = category_links(base_url) 
    for categorie in categories.keys():
        print("categories[categorie] ====>>>", categories[categorie])
        links = pages_livre(categories[categorie])
        info = info_from_category(links)
        
        # write_csv(info, categorie)