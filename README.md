# PROJET-IOT

Ce projet vise à faciliter l'intégration de dispositifs IoT avec Chirpstack en utilisant une combinaison d'un serveur Chirpstack, une API REST, et un serveur chirpstack-rest-api.

# Fonctionnalités
Utilisation d'un serveur Chirpstack pour la gestion des dispositifs IoT.
Communication avec Chirpstack via son API REST.
Installation et utilisation d'un serveur chirpstack-rest-api pour communiquer avec Chirpstack (qui ne supporte plus nativement REST depuis la version v4 de chirpstack).
Implémentation en Python pour récupérer les informations d'un capteur à partir d'une webcam.
Les informations récupérées (DEV EUI, APP EUI, APP KEY, APPSKEY, NETSKEY) sont enregistrées dans un fichier CSV.
Un script Python supplémentaire utilise les informations du CSV pour enregistrer le dispositif dans le serveur Chirpstack.

# Prérequis
Avant de commencer, assurez-vous d'avoir installé les éléments suivants :
Serveur Chirpstack
Python ( librairie 
Webcam ou téléphone 
Serveur rest-grpc

https://www.chirpstack.io/docs/chirpstack/downloads.html#debian--ubuntu-repositoryhttps://github.com/chirpstack/chirpstack-rest-api
c’est un logiciel qui transforme le code rest en grpc vers Rest 

serveur chipstak : 192.168.170.223:8080

api token (ou bearer) : 
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6IjBkNGU5NGU2LTExNGQtNGIxMC04YTlkLTA3MTViODE4Mzc0ZCIsInR5cCI6ImtleSJ9.oS3z2Dw1lSZ7s5r9QTl1kX9aHjQgqGiFSSsVs3BYTZc

# Installation 

## Serveur rest-grpc
Depuis la version v4 de chirstack , l'api rest n'est plus pris en charge nativement.
https://www.chirpstack.io/docs/chirpstack/api/rest.html

Un projet GitLab existe qui permet de créer notre propre serveur chirpstack-rest-api qui permet de contourner le problème 
https://github.com/chirpstack/chirpstack-rest-api?tab=readme-ov-file

Dans notre projet nous avons décider d'utiliser les repos directement
https://www.chirpstack.io/docs/chirpstack/downloads.html#debian--ubuntu-repositoryhttps://github.com/chirpstack/chirpstack-rest-api

### Configuration pour récupérer le repos
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 1CE2AFD36DBCCA00
sudo echo "deb https://artifacts.chirpstack.io/packages/4.x/deb stable main" | sudo tee /etc/apt/sources.list.d/chirpstack_4.list
sudo apt update

### Installation du serveur 

sudo apt install chirpstack-rest-api

### Configuration du serveur

Il faut configurer le port et l'IP du serveur chirtsack-rest-api  et du serveur chirpstack
Le plus simple est d'installer chirpstack-rest-api directement sur le serveur où se trouve chirpstack 
Il faut modifier le fichier suivant :
/etc/chirpstack-rest-api/environment

BIND=0.0.0.0:8090
SERVER=0.0.0.0:8080

BIND = serveur chirpstack-rest-api
SERVEUR = chirpstack
"# Comment out to enable TLS
INSECURE=true

Attention : il faut que le port ne soit pas déjà en écoute.
netstat -tuln 
### Commande pour gerer le service 
sudo systemctl [restart|start|stop] chirpstack-rest-api

## Choix de la caméra
Il est possible d'utiliser une webcam dédié ou directement votre téléphone, nous vous recommandons d'avoir à minima une qualité d'affiche en full hd en 1080p pour que l'OCR puisse être efficace.

Si vous faites le choix d'une webcam, sa mise en place est plug and play, vous avez juste à la brancher à l'ordinateur et de choisir lors du lancement du script "ocr-lorawan-devices.py" le bon numéro d'index correspond à la caméra. En fonction du modèle de webcam utilisé et si elle le permet, vous pouvez installer le logiciel du constructeur pour la piloter, par exemple pour la webcam logitech C920, le logiciel "LogiTune" permet de régler certains paramètres à la volet telle que le focus, le zoom, le constraste etc...




