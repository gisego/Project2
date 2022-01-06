import requests
from bs4 import BeautifulSoup
from pathlib import Path
import wget
import csv



# Etape 1
# Ecrire une fonction category(base_url) qui retourne les liens des categories dans un dictionnaire. Ex: return {"travel": 'http://books.toscrape.com/travel......'}
#
def category():
    base_url = 'http://books.toscrape.com'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    uls = soup.find('ul', class_= 'nav nav-list')
    all_a = uls.find_all('a')
    my_dictionnaire = {}
    for hrefs in all_a:
        category_name = hrefs.text
        category_name = category_name.replace('\n', '')
        category_name = category_name.replace(' ', '')
        href = hrefs['href']
        hrefs = base_url + '/' + href
        my_dictionnaire[category_name] = hrefs
    my_dictionnaire.pop('Books')
    return my_dictionnaire


# Etape 2 Ecrire une fonction pages_livre(url_category) qui prend en parametre l'url d'une categorie Et qui retourne l'url de tous les livres de cette categorie sous forme de list.
# Ex: return [http: // books.toscrape.com / travel / .... /, http: // books.toscrape.com / travel / .... /]

def page_book(url_category):
    links_books = []
    r = requests.get(url_category)
    soup = BeautifulSoup(r.content, 'html.parser')
    num_page = soup.find('li', class_='current')
    categories = str(url_category.replace('/index.html', ''))
    if r.ok:
        if num_page is not None:
            num_page = (soup.find('li', class_='current').text).replace(' ','')[9]
            for num_page in range(int(num_page)):
                url = categories+'/page-' + str(num_page+1) + '.html'
                re = requests.get(url)
                soup1 = BeautifulSoup(re.content, 'html.parser')
                if re.ok:
                    for links_pages in soup1.find_all("div", class_= "image_container"):
                        for allas in links_pages.find_all('a'):
                            links_pages = allas['href'].replace('../../../', 'http://books.toscrape.com/catalogue/')
                        links_books.append(links_pages)
        else:
            for links in soup.find_all("div", class_="image_container"):
                for alls in links.find_all('a'):
                    links_simple = alls['href'].replace('../../../', 'http://books.toscrape.com/catalogue/')
                links_books.append(links_simple)
    return links_books



# # # Etape 3  Ecrire fonction Write_image(lien_image_livre, nom_categorie)# qui utilise path et wget pour classer en fonction des parametres "lien_image_livre, nom_categorie"
#
def download_image(image_url, category):
    base_image = 'images'
    path = f'{base_image}/{category}'
    Path(path).mkdir(parents=True, exist_ok=True)
    wget.download(image_url, path, bar=None)

def info_from_category(links):
    infos = []
    for link in links:
        book_info = book(link)
        infos.append(book_info)
        download_image(book_info['image_url'], book_info['category'])
    return infos

# # # Etape 4 Ecrire # une fonction livre(lien_un_livre) qui recupere les infos du livre  et retourne les infos du livre dans un dictionnaire.
#
def book(book_link):
    dictionnaire = {}
    r = requests.get(book_link)
    soup = BeautifulSoup(r.content, 'html.parser')
    product_page_url = r.url
    dictionnaire['product_page'] = product_page_url
    title = soup.find('title').getText()
    title = title.replace('\n', '')
    title = ''.join(title)
    dictionnaire['title'] = title
    image_url = soup.find("img")["src"]
    image_url = "http://books.toscrape.com" + image_url
    image_url = image_url.split('../..')
    image_url = ''.join(image_url)
    dictionnaire['image_url'] = image_url
    product_description = soup.find("p", class_="")
    dictionnaire['description'] = product_description
    ultag = soup.find("ul", class_="breadcrumb")
    category = ultag.find_all("li")[2].text
    category= category.replace('\n', '')
    dictionnaire['category'] = category
    tds = soup.find_all("td")
    universal_product_code = tds[0].text
    dictionnaire['universal_code'] = universal_product_code
    price_excluding_tax = tds[2].text
    dictionnaire['price_excluding_tax'] = price_excluding_tax
    price_including_tax = tds[3].text
    dictionnaire['Price_including_tax'] = price_including_tax
    number_available = tds[5].text
    dictionnaire['number_available'] = number_available
    review_rating = tds[6].text
    dictionnaire['review_Rating'] = review_rating
    return dictionnaire
#
# # # # Etape 5 Ecrire une fonction write_csv(infos_livre, nom categorie) qui ouvre un fichier csv avec pour nom la categorie passé en parametre, puis enregistre les infos "infos_livre" recu dans
# # # # le csv.
# #
titles =['product_page_url',
            'universal_product_code',
            'title',
            'price_including_tax',
            'price_excluding_tax',
            'number_available',
            'product_description',
            'category',
            'review_rating',
            'image_url']

def write_csv(info_book, name_category):
    file_csv = name_category + '.csv'
    with open(file_csv, 'w', newline='', encoding='iso-8859-1') as files_csv:
        write = csv.DictWriter(files_csv, fieldnames=titles)
        write.writeheader()
        # for info_books in info_book:
        write.writerow({'product_page_url': info_book['product_page_url'],
                             'universal_product_code': info_book['universal_product_code'],
                             'title': info_book['title'],
                             'price_including_tax': info_book['price_including_tax'].strip(),
                             'price_excluding_tax': info_book['price_excluding_tax'].strip(),
                             'number_available': info_book['number_available'].strip(),
                             'product_description': str(info_book['product_description']),
                             'category': info_book['category'].strip(),
                             'review_rating': info_book['review_rating'].strip(),
                             'image_url': info_book['image_url']})

# # #### Exemple TEST
#
# info_book = {'product_page_url': 'testurl', 'universal_product_code': 'UPC', 'title': 'titre', 'price_including_tax': 'price_in',
#          'price_excluding_tax': 'price_ex', 'number_available': 'available', 'product_description': 'descrip',
#          'category': 'cat', 'review_rating': 'rating', 'image_url': 'image'}
#
# name_category = "Cat"
#
# print(write_csv(info_book, name_category))


# #
# # # Etape 6 Organiser toutes les fonctions dans le main du fichier.
if __name__ == '__main__':
    categories = category()
    for category in categories.keys():
        links = page_book(categories[category])
        info = info_from_category(links)
    write_csv(info, category())
