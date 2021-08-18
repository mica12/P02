import requests
from bs4 import BeautifulSoup
import csv

url='http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

en_tete=['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available','product_description', 'category', 'review_rating', 'image_url']

response= requests.get(url)

soup=BeautifulSoup(response.content, features="html.parser")



#recuperer tableau qui contient les informations produit
table=soup.find_all("td")

#recuperer upc(code produit) dans la table
upc=table[0].text

#recuperer titre
titre=soup.find('h1')
titre=titre.text

#recuperer image url
images=soup.find('img')
lien_image=images["src"]
lien_image=lien_image.replace('../..', 'https://books.toscrape.com')


#recuperer price_including_tax dans la table
prix_TTC=table[3].text


#recuperer price_excluding_tax dans la table
prix_HT=table[2].text

#recuperer number_available dans la table
stock=table[5].text

#recuperer product_description
meta=soup.find_all("meta")
description=meta[2]
description=str(description)
description=description.replace('<meta content="', ' ')
description=description.replace('" name="description"/>', ' ')

#recuperer category
lis=soup.findAll("li")
category=lis[2].text
	
#recuperer review_rating dans la table
review_rating=table[6].text	


with open('extraction_un_livre.csv', 'w') as csv_file:
	writer=csv.writer(csv_file, delimiter=',')
	writer.writerow(en_tete)



print(url)
print(upc)
print(titre)
print(prix_TTC)
print(prix_HT)
print(stock)
print(description)
print(category)
print(review_rating)
print(lien_image)



