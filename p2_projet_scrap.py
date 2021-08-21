import requests
from bs4 import BeautifulSoup
import csv
from math import *
import os


if not os.path.exists("images"):
    os.makedirs("images")
if not os.path.exists("csv"):
    os.makedirs("csv")


# parser la page page d'accueil du site pour recuperer l'ensemble des categories

url = "https://books.toscrape.com/index.html"

response_url = requests.get(url)

soup_url = BeautifulSoup(response_url.content, features="html.parser")


# recuperation des adresses https de chaque category dans le site
liens_category = []
noms_category = []
extraits_lien_categorie = []
ul_balises = soup_url.findAll("ul", class_="nav nav-list")


for ul_balise in ul_balises:  # recherche des balises <a>
    a = ul_balise.find_all("a")

# cette boucle permet de recuperer les liens des categories mais aussi les noms des categories qui serviront au nomage des fichiers csv
for k in range(len(a) - 1):
    l = k + 1
    lien_category = a[l]
    lien_category = lien_category["href"]
    lien_category = ("https://books.toscrape.com/" + lien_category)  # on recupere ici le lien qui servira pour scraper une categorie si celle ci contient une page
    liens_category.append(lien_category)
    nom_category = a[l].text  # on recupere ici le nom qui servira pour crée un fichier csv par categorie
    nom_category = nom_category.replace(" ", "")
    nom_category = nom_category.replace("\n", "")
    noms_category.append(nom_category)
    extrait_lien_categorie = (lien_category)  # on recupere ici un extrait du lien qui servira pour scraper une categorie si celle ci contient plus d'une page
    extrait_lien_categorie = extrait_lien_categorie.replace("https://books.toscrape.com/catalogue/category/books/", "")
    extrait_lien_categorie = extrait_lien_categorie.replace("/index.html", "")
    extraits_lien_categorie.append(extrait_lien_categorie)
# fin boucle for

# debut de boucle pour parser l'ensemble du site et creer les csv de chaque categorie
for m in range(len(liens_category)):
    nom_fichier_csv = "extraction_une_categorie_" + noms_category[m] + ".csv"

    # en tete d'un fichier csv
    en_tete = [
        "product_page_url_un_livre",
        "upc",
        "title",
        "price_including_tax",
        "price_excluding_tax",
        "number_available",
        "product_description",
        "category",
        "review_rating",
        "image_url_un_livre",
    ]

    # creation du fichier csv avec ajout de en tete
    # nom_du_fichier=''
    with open("csv/" + nom_fichier_csv, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(en_tete)

    # parser la page categorie pour recuperer le nombre de page pour une categorie

    url_une_category = liens_category[m]

    response_une_category = requests.get(url_une_category)

    soup_page_une_category = BeautifulSoup(response_une_category.content, features="html.parser")

    # calcul du nombre de page par categorie
    strong_balises = soup_page_une_category.findAll("strong")
    nombre_de_livre_pour_une_categorie = float(strong_balises[1].text)
    nombre_de_page_pour_une_categorie = ceil(nombre_de_livre_pour_une_categorie / 20)  # 20 livre par page maximum

    # parser l'ensemble des pages d'une categorie
    for i in range(nombre_de_page_pour_une_categorie):
        j = i + 1
        if nombre_de_page_pour_une_categorie > 1:
            url_une_category = ("https://books.toscrape.com/catalogue/category/books/" + extraits_lien_categorie[m] + "/page-" + str(j) + ".html")
        response_une_category = requests.get(url_une_category)
        soup_page_une_category = BeautifulSoup(response_une_category.content, features="html.parser")

        # recuperation des adresses https de chaque livre dans une categorie choisie
        links = []
        h3_balises = soup_page_une_category.findAll("h3")

        for h3_balise in h3_balises:
            a = h3_balise.find("a")
            link = a["href"]
            link = link.replace("../../../", "https://books.toscrape.com/catalogue/")
            links.append(link)
        # fin boucle balises h3

        nombre_de_lien_par_page = len(links)

        for i in range(nombre_de_lien_par_page):

            url_un_livre = links[i]

            response = requests.get(url_un_livre)

            soup_page_un_livre = BeautifulSoup(response.content, features="html.parser")
            # fin boucle nombre_de_lien_par_page

            # recuperer tableau qui contient les informations produit
            table = soup_page_un_livre.find_all("td")

            # recuperer upc(code produit) dans la table
            upcs = table[0].text

            # recuperer titre
            titres = soup_page_un_livre.find("h1")
            titres = titres.text

            # recuperer image url_un_livre
            images = soup_page_un_livre.find("img")
            lien_images = images["src"]
            lien_images = lien_images.replace("../..", "https://books.toscrape.com")

            # recuperer price_including_tax dans la table
            prix_TTCs = table[3].text

            # recuperer price_excluding_tax dans la table
            prix_HTs = table[2].text

            # recuperer number_available dans la table
            stocks = table[5].text

            # recuperer product_description
            meta = soup_page_un_livre.find_all("meta")
            descriptions = meta[2]
            descriptions = str(descriptions)
            descriptions = descriptions.replace('<meta content="', " ")
            descriptions = descriptions.replace('" name="description"/>', " ")

            # recuperer category
            lis = soup_page_un_livre.findAll("li")
            categorys = lis[2].text

            # recuperer review_rating dans la table
            review_ratings = table[6].text

            # on cree une liste contenant toutes les informations sur un livre
            ligne = []
            ligne.append(url_un_livre)
            ligne.append(upcs)
            ligne.append(titres)
            ligne.append(prix_TTCs)
            ligne.append(prix_HTs)
            ligne.append(stocks)
            ligne.append(descriptions)
            ligne.append(categorys)
            ligne.append(review_ratings)
            ligne.append(lien_images)

            # ecriture de la liste dans le fichier csv crée auparavant
            with open("csv/" + nom_fichier_csv, "a") as csv_file:
                writer = csv.writer(csv_file, delimiter=",")
                writer.writerow(ligne)

            # telechargement des images
            nom_fichier_image = titres + ".jpg"
            nom_fichier_image = nom_fichier_image.replace("/", "-")
            f = open("images/" + nom_fichier_image, "wb")
            response = requests.get(lien_images)
            f.write(response.content)
            f.close()

        # fin boucle for parser l'ensemble des pages d'une categorie
