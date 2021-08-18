import requests
from bs4 import BeautifulSoup
import csv

urls='http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

en_tete=['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available','product_description', 'category', 'review_rating', 'image_url']

response= requests.get(urls)

soup=BeautifulSoup(response.content, features="html.parser")



#recuperer tableau qui contient les informations produit
table=soup.find_all("td")

#recuperer upc(code produit) dans la table
upcs=table[0].text

#recuperer titre
titres=soup.find('h1')
titres=titres.text

#recuperer image url
images=soup.find('img')
lien_images=images["src"]
lien_images=lien_images.replace('../..', 'https://books.toscrape.com')


#recuperer price_including_tax dans la table
prix_TTCs=table[3].text


#recuperer price_excluding_tax dans la table
prix_HTs=table[2].text

#recuperer number_available dans la table
stocks=table[5].text

#recuperer product_description
meta=soup.find_all("meta")
descriptions=meta[2]
descriptions=str(descriptions)
descriptions=descriptions.replace('<meta content="', ' ')
descriptions=descriptions.replace('" name="description"/>', ' ')
"""liste=[]
liste.append(descriptions)
descriptions=liste[0]"""

#recuperer category
lis=soup.findAll("li")
categorys=lis[2].text
	
#recuperer review_rating dans la table
review_ratings=table[6].text	

ligne=[]
ligne.append(urls)
ligne.append(upcs)
ligne.append(titres)
ligne.append(prix_TTCs)
ligne.append(prix_HTs)
ligne.append(stocks)
ligne.append(descriptions)
ligne.append(categorys)
ligne.append(review_ratings)
ligne.append(lien_images)

with open('extraction_un_livre.csv', 'w') as csv_file:
	writer=csv.writer(csv_file, delimiter=',')
	writer.writerow(en_tete)
	writer.writerow(ligne)


	"""for url,upc,titre,prix_TTC,prix_HT,stock,description,category,review_rating,lien_image in zip(urls,upcs,titres,prix_TTCs,prix_HTs,stocks,descriptions,categorys,review_ratings,lien_images):
		writer.writerow([url,upc,titre,prix_TTC,prix_HT,stock,description,category,review_rating,lien_image])"""


print(urls)
print(upcs)
print(titres)
print(prix_TTCs)
print(prix_HTs)
print(stocks)
print(descriptions)
print(categorys)
print(review_ratings)
print(lien_images)



