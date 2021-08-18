import requests
from bs4 import BeautifulSoup
import csv
from math import *

#en tete du fichier csv
en_tete=['product_page_url_un_livre', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available','product_description', 'category', 'review_rating', 'image_url_un_livre']

#creation du fichier csv avec ajout de en tete
with open('extraction_une_categorie.csv', 'w') as csv_file:
	writer=csv.writer(csv_file, delimiter=',')
	writer.writerow(en_tete)
		

#parser la page categorie pour recuperer le nombre de page pour une categorie

url_une_category='https://books.toscrape.com/catalogue/category/books/mystery_3/page-1.html'

response_une_category= requests.get(url_une_category)

soup_page_une_category=BeautifulSoup(response_une_category.content, features="html.parser")

#calcul du nombre de page par categorie
strong_balises=soup_page_une_category.findAll('strong')
nombre_de_livre_pour_une_categorie=float(strong_balises[1].text)
nombre_de_page_pour_une_categorie=ceil(nombre_de_livre_pour_une_categorie/20) #20 livre par page maximum


#parser l'ensemble des pages d'une categorie
for i in range(nombre_de_page_pour_une_categorie):
	j=i+1
	url_une_category='https://books.toscrape.com/catalogue/category/books/mystery_3/page-'+str(j)+'.html'
	response_une_category= requests.get(url_une_category)
	soup_page_une_category=BeautifulSoup(response_une_category.content, features="html.parser")

	#recuperation des adresses https de chaque livre dans une categorie choisie
	links=[]

	h3_balises=soup_page_une_category.findAll('h3')
	for h3_balise in h3_balises:
		a=h3_balise.find('a')
		link=a['href']
		link=link.replace('../../../', 'https://books.toscrape.com/catalogue/')
		links.append(link)

	nombre_de_lien_par_page=len(links)


	
	for i in range(nombre_de_lien_par_page):

		url_un_livre=links[i]	

		response= requests.get(url_un_livre)

		soup_page_un_livre=BeautifulSoup(response.content, features="html.parser")



		#recuperer tableau qui contient les informations produit
		table=soup_page_un_livre.find_all("td")

		#recuperer upc(code produit) dans la table
		upcs=table[0].text

		#recuperer titre
		titres=soup_page_un_livre.find('h1')
		titres=titres.text

		#recuperer image url_un_livre
		images=soup_page_un_livre.find('img')
		lien_images=images["src"]
		lien_images=lien_images.replace('../..', 'https://books.toscrape.com')


		#recuperer price_including_tax dans la table
		prix_TTCs=table[3].text


		#recuperer price_excluding_tax dans la table
		prix_HTs=table[2].text

		#recuperer number_available dans la table
		stocks=table[5].text

		#recuperer product_description
		meta=soup_page_un_livre.find_all("meta")
		descriptions=meta[2]
		descriptions=str(descriptions)
		descriptions=descriptions.replace('<meta content="', ' ')
		descriptions=descriptions.replace('" name="description"/>', ' ')
		
		#recuperer category
		lis=soup_page_un_livre.findAll("li")
		categorys=lis[2].text
			
		#recuperer review_rating dans la table
		review_ratings=table[6].text	

		ligne=[]
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

		with open('extraction_une_categorie.csv', 'a') as csv_file:
			writer=csv.writer(csv_file, delimiter=',')
			writer.writerow(ligne)


	"""test print
	print(url_un_livre)
	print(upcs)
	print(titres)
	print(prix_TTCs)
	print(prix_HTs)
	print(stocks)
	print(descriptions)
	print(categorys)
	print(review_ratings)
	print(lien_images)"""
	


