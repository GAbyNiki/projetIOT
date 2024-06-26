# PROJET IOT

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
```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 1CE2AFD36DBCCA00
sudo echo "deb https://artifacts.chirpstack.io/packages/4.x/deb stable main" | sudo tee /etc/apt/sources.list.d/chirpstack_4.list
sudo apt update
```

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
```bash
netstat -tuln
```

### Génération de la clé API

Pour générer une nouvelle clé API avec le token (ou bearer) associé, il faut se rendre sur l'interface web du server Chirpstack (@IP:8080 du serveur)

- Sous la section "Network Server", sélectionner "API Keys", puis "Add API key".
- Assigner un nom à la clé API puis faire "submit"
- Le token (ou bearer) est ensuite affiché, il faut bien le sauvegarder car il sera affiché une seule fois, puis le renseigner dans le fichier informations.csv

### Commande pour gerer le service
```bash
sudo systemctl [restart|start|stop] chirpstack-rest-api
```

## Choix de la caméra
Il est possible d'utiliser une webcam dédiée ou directement votre téléphone, nous vous recommandons d'avoir à minima une qualité d'affiche en full hd en 1080p pour que l'OCR puisse être efficace.

Si vous faites le choix d'une webcam, sa mise en place est plug and play, vous avez juste à la brancher à l'ordinateur et de choisir lors du lancement du script "ocr-lorawan-devices.py" le bon numéro d'index correspond à la caméra. En fonction du modèle de webcam utilisé et si elle le permet, vous pouvez installer le logiciel du constructeur pour la piloter, par exemple pour la webcam logitech C920, le logiciel "LogiTune" permet de régler certains paramètres à la volet telle que le focus, le zoom, le constraste etc...

Si votre choix se porte sur l'utilisation d'un téléphone, la mise en place nécessite quelques manipulations. Nous vous recommandons d'utiliser un câble USB pour la connexion entre votre PC et le portable. Si vous possédez un téléphone Google Pixel sous Android 14 minimum, vous avez la possibilité nativement d'utiliser la caméra du téléphone en tant que webcam, pour cela vous devez brancher votre téléphone à l'ordinateur, lorsque la notification de branchement USB est affiché sur le téléphone, cliquer dessus pour afficher les options supplémentaires et choisissez l'option "Utilisé USB pour Webcam", vous n'avez rien d'autres à faire (remarques: l'utilisation de cette méthode ne permet pas d'obtenir une qualité optimale, la seconde option avec une application tierce permet de profiter pleinement d'une qualité optimale). 

La seconde méthode avec un téléphone autre que Google, consiste à télécharger sur le Google Playstore l'application "DroidCam Webcam" (cf. https://play.google.com/store/apps/details?id=com.dev47apps.droidcam&hl=fr&gl=US&pli=1) et également sur votre ordinateur Windows (cf. https://www.dev47apps.com/droidcam/windows/). Avant l'exécution du script "ocr-lorawan-devices.py", lancer sur votre téléphone l'application "DroidCam Webcam" (remarques: pour obtenir la meilleure qualité possible, vous pouvez visionner une pub de 30 secondes environ et profiter du mode HD pendant 1 heure, pour cela il faut cliquer sur l'icône "HD" en haut à droite sur la page d'accueil). Lancer aussi le logiciel "DroidCam Client" sur votre ordinateur Windows, une fenêtre contextuelle s'ouvre, sélectionner le logo USB et appuyer sur le bouton "refresh" et patienter 10 secondes (Attention si c'est la première fois que vous utilisez l'application un pop-up apparaîtra sur votre téléphone vous demandant d'accepter la connexion) :

![image](https://github.com/GAbyNiki/projetIOT/assets/79327440/a1a5dc44-c4c4-4f5c-babf-0f68bb5561c5)

Vous devez maintenant voir apparaître votre téléphone :

![image](https://github.com/GAbyNiki/projetIOT/assets/79327440/78ba38f1-ab00-48f0-abc0-1821dad960fd)

Il ne vous reste plus qu'à cliquer sur "Start" et lancer le code python !

# Utilisation 

Nous avons créé un exécutable exe qui permet de lancer les scripts même si python ou les librairies ne sont pas installé directement sur la machine

Nous avons plusieurs scripts

### ocr-lorawan-devices.py

En résumé ce code python permet de réaliser les actions suivantes :
- d'ouvrir un flux vidéo via une caméra externe
- de prendre une capture d'écran à n'importe quel instant sur le flux vidéo récupérée
- lancer une requête de type OCR sur les images capturées pour y extraire le texte
- parser et formater les données récupérées dans un fichier CSV pour une utilisation à postériori dans le script add-devices.py

Nous utilisons l'API Google Cloud Vision, il s'agit de la solution qui a fournis les meilleures résultats dans nos différents tests pour la reconnaissance des caractères. Nous vous recommandons de consulter ces différentes documentations avant de continuer la procédure : https://cloud.google.com/vision/pricing?hl=fr et https://cloud.google.com/vision/docs/data-usage?hl=fr. Pour sa mise en place vous devez posséder un compte Google et vous connecter sur la console Google Cloud : https://console.cloud.google.com/ (Google exige l'ajout de sa CB, en terme Goolge il s'agit d'un "compte de facturation" pour utiliser leur API mais cela ne signifie pas que vous serez facturer si vous respecter les quotas d'utilisations de l'API). Une fois connecter créer un projet sur l'interface, par exemple OCR-LoraWan (cf. https://cloud.google.com/resource-manager/docs/creating-managing-projects?hl=fr).

![image](https://github.com/GAbyNiki/projetIOT/assets/79327440/43e6a495-7066-459c-848f-526045f6797a)

Vous devez à présent activer l'API Google Cloud Vision, pour cela rendez-vous dans votre projet et dans le menu "API et services" :

![image](https://github.com/GAbyNiki/projetIOT/assets/79327440/06d127a9-9630-4a5f-91c6-0737964f44a9)

Cliquer ensuite sur "Activer les API et les services" et renseigner dans la barre de recherche "cloud vision api" :

![image](https://github.com/GAbyNiki/projetIOT/assets/79327440/fcd74da1-a1c2-4b06-9cb5-bf162ec8dff5)

Puis :

![image](https://github.com/GAbyNiki/projetIOT/assets/79327440/22f86ea2-81ae-4eec-9c5a-6b78ae0e3e0a)

Et activer l'API :

![image](https://github.com/GAbyNiki/projetIOT/assets/79327440/7348d714-cd15-43a4-8798-bc246c91284f)

Lors de l'activation de l'API un pop-up apparaîtra pour créer votre identifiant lié à l'API (si le pop-up n'apparaît pas rendez-vous dans le menu "identifiant" à gauche dans le menu), cet identifiant est nécessaire pour authentifier chaque requête envoyé par le script. ATTENTION : Choisissez bien un identifiant de type "compte de service" :

![image](https://github.com/GAbyNiki/projetIOT/assets/79327440/ee31b0b4-a57a-4f8a-98a5-30b0019c1050)

Vous pouvez cliquer sur "continuer" ensuite jusqu'à la fin du "wizard".

Cliquer sur le compte de service précédemment créé :

![image](https://github.com/GAbyNiki/projetIOT/assets/79327440/681f43f6-16ad-4484-981e-74bd68e66137)

Et créer votre clé privée au format json :

![image](https://github.com/GAbyNiki/projetIOT/assets/79327440/2aff62e5-0dba-4968-9842-b66f8cc670a6)

Lorsque votre explorateur Windows s'ouvre pour sauvegarder la clé json, renommer la sous le nom "token.json" et stocker la dans la racine où se trouve le code "ocr-lorawan-devices.py".


### get-devices.py

Permet de récupérer les informations de tous les devices du serveur chirpstack
Cela crée un fichier devices.csv où se trouve les differentes informations des devices 

devEui
createdAt
updatedAt
lastSeenAt
name
description
deviceProfileId
deviceProfileName
deviceStatus


### add-devices.py
Ce script permet à partir du fichier Informations.csv  et du fichier extracted_data.csv de remplir automatiquement les devices sur chirpstack.

1 - rentrer les informations dans le fichier informations.txt. 
SERVER_IP : l'adresse IP ou se trouve le serveur chirpstack
BEARER : Le token API  du serveur chirpstack
APP_ID : L'ID de l'application où les devices vont être provisionés
PROFILE_ID : l'ID du PROFIL_ID

2 - Lancer le script 




