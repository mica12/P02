# P02
P02 SCRAPPING

Que fait le programme?:

le programme scrap le site : http://books.toscrape.com/ 
ce site site est une plateforme qui vend des livre
le programme recupere divers informations sur chaque livre et les ecrit dans des fichiers csv
les livres étant classés par categorie un csv est crée par categorie
le programme recupere aussi les images des couverture de chaque livre et les enregistre au format jpg.
les fichiers image sont stockés dans un repertoire image et les fichiers csv sont stocké dans un fichier csv

Comment lancer le programme?

Etape1:
telecharger le repertoire P02-main.zip depuis github puis le decompresser


Etape2:
placer vous dans le repertoire /P02-main depuis votre terminal de commande
Puis activer un environement virtuel à l'aide des commandes :

python -m venv env 
source env/bin/activate(sous linux)
env/Scripts/activate.bat(sous windows)

Etape 3 :
installer les bibliotheque requises(cf. fichier requirements.txt)
taper les commandes dans le terminal:
pip install requests
pip install bs4

Etape4 : executer le programme
dans le terminal de commande ecrire :
python3 p2_projet_scrap.py(sous linux)
python p2_projet_scrap.py(sous windows)



