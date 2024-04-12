import io
import os
import re
import csv
import cv2
from google.cloud import vision

# Répertoire de travail actuel
current_working_directory = os.getcwd()

try:
    if not os.path.exists(current_working_directory + '\\token.json'):
        raise FileNotFoundError("Le fichier token.json n'existe pas dans le dossier :" + current_working_directory + ". Veuillez vous assurer de fournir ce fichier en le téléchargeant sur votre profil Google Cloud et en le renommant token.json")
except FileNotFoundError as e:
    print(e)
    exit()
except Exception as e:
    print("Une erreur s'est produite:", e)

# Configuration des identifiants d'authentification pour la Vision API de Google
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'token.json'

# Chemin vers le répertoire contenant les images
image_path = current_working_directory + '\\Images\\'

# Fonction pour extraire les données hexadécimales et les identifiants de périphérique
def extract_hexadecimal(text):
    # Motif pour les données hexadécimales - exclusivement des caractères héxas de 16 ou 32 caractères
    hex_pattern = r'\b(?:[0-9a-fA-F]{16}|[0-9a-fA-F]{32})\b'
    # Motif pour l'identifiant de périphérique - exclusivement des chiffres de 0 à 9 de 3 caractères
    dev_id_pattern = r'\b(?:[0-9]{3})\b'
    # Recherche des données hexadécimales et de l'identifiant de périphérique dans le texte donné
    dev_id = re.findall(dev_id_pattern, text)
    hexadecimal_data = re.findall(hex_pattern, text)
    return hexadecimal_data[:3], dev_id[0]

# Fonction pour sauvegarder les données extraites dans un fichier CSV
def save_to_csv(dev_id, dev_eui, app_eui, app_key, dev_id_confidence, dev_eui_confidence, app_eui_confidence, app_key_confidence):
    with open('extracted_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([dev_id, dev_eui, app_eui, app_key, dev_id_confidence, dev_eui_confidence, app_eui_confidence, app_key_confidence])

# Fonction pour détecter du texte dans une image et sauvegarder les informations pertinentes
def detect_text_and_save(image_path):
    # Initialisation des confidences à None
    dev_id_confidence = None
    dev_eui_confidence = None
    app_eui_confidence = None
    app_key_confidence = None

    # Initialisation du client de la Vision API de Google
    client = vision.ImageAnnotatorClient()

    try:
        # Lecture de l'image
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        # Création de l'objet Image pour la Vision API
        image = vision.Image(content=content)
        # Paramètres pour activer la détection de texte avec la confiance
        text_detection_params = vision.TextDetectionParams(enable_text_detection_confidence_score=True)
        image_context = vision.ImageContext(text_detection_params=text_detection_params)
        # Détection du texte dans l'image
        ocr_response = client.text_detection(image=image, image_context=image_context)
        texts = ocr_response.text_annotations
        if texts:
            detected_text = texts[0].description
            
            # Extraction des données hexadécimales et de l'identifiant de périphérique
            hexadecimal_data, dev_id = extract_hexadecimal(detected_text)
            
            # Remplissage des données hexadécimales manquantes avec des chaînes vides
            while len(hexadecimal_data) < 3:
                hexadecimal_data.append('')
            
            # Si l'identifiant de périphérique est une liste, prendre le premier élément
            if isinstance(dev_id, list):
                dev_id = dev_id[0]
            
            # Séparation des données hexadécimales en variables distinctes
            dev_eui, app_eui, app_key = hexadecimal_data
            confidence = []

            # Récupération du taux de confiance pour chaque mot dans l'image
            for page in ocr_response.full_text_annotation.pages:
                for block in page.blocks:
                    for paragraph in block.paragraphs:                   
                        for word in paragraph.words:
                            word_text = ''.join([
                                symbol.text for symbol in word.symbols
                            ])
                            if word_text == dev_id:
                                confidence.append(word.confidence)
                            for data in hexadecimal_data:
                                if word_text == data:
                                    confidence.append(word.confidence)
            i = 0
            # Affectation des confidences avec un avertissement si elles sont inférieures à 0.95
            for c in confidence:
                if c < 0.95:
                    if i == 0:
                        dev_id_confidence = f"Warning {c*100:.2f}%"
                    elif i == 1:
                        dev_eui_confidence = f"Warning {c*100:.2f}%"
                    elif i == 2:
                        app_eui_confidence = f"Warning {c*100:.2f}%"
                    elif i == 3:
                        app_key_confidence = f"Warning {c*100:.2f}%"
                else:
                    if i == 0:
                        dev_id_confidence = f"{c*100:.2f}%"
                    elif i == 1:
                        dev_eui_confidence = f"{c*100:.2f}%"
                    elif i == 2:
                        app_eui_confidence = f"{c*100:.2f}%"
                    elif i == 3:
                        app_key_confidence = f"{c*100:.2f}%"   
                i += 1

            # Enregistrement dans le CSV des informations récupérées via l'OCR
            save_to_csv(dev_id, dev_eui, app_eui, app_key, dev_id_confidence, dev_eui_confidence, app_eui_confidence, app_key_confidence)
        else:
            raise ValueError("Pas de texte détecté sur l'image")
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier '{image_path}' n'existe pas.")
    except Exception as e:
        raise Exception(f"Une erreur s'est produite: {str(e)}")
    else:
        if ocr_response.error.message:
            raise Exception(f"Erreur dans Google Vision API: {ocr_response.error.message}")
    
    return dev_id, dev_eui, app_eui, app_key, dev_id_confidence, dev_eui_confidence, app_eui_confidence, app_key_confidence

# Fonction pour ouvrir le flux vidéo de la caméra, capturer des images et les traiter
def open_camera(index_camera):
    # Initialisation de la capture vidéo
    cap = cv2.VideoCapture(index_camera)

    # Vérification si la caméra est ouverte
    if not cap.isOpened():
        print("Erreur: L'ouverture de la caméra a échoué. Veuillez vérifier si la caméra est connectée et/ou essayer un autre index.")
        exit()

    # Boucle pour capturer les images en continu
    i=0    
    while True:
        # Capture de l'image
        ret, frame = cap.read()

        # Vérification si l'image est correctement capturée
        if not ret:
            print("Erreur dans l'ouverture du flux vidéo.")
            break

        # Affichage de l'image capturée
        cv2.imshow('Video', frame)

        # Attente de l'appui sur une touche du clavier
        key = cv2.waitKey(1)
        if key & 0xFF == ord('w'):
            # Nom de fichier pour l'image, ce nom est temporaire il est ensuite renommé plus bas
            image_filename = f'DEV-{i}.jpg'
            # Sauvegarde de l'image
            cv2.imwrite(image_path + image_filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            try:
                # Traitement de l'image capturée
                device_info = detect_text_and_save(image_path + image_filename)
                # Affichage des informations extraites
                print("DEVICE ID: " + device_info[0]  +  " | DEV EUI: " + device_info[1] + " | APP EUI: " + device_info[2] + " | APP KEY: " + device_info[3] + " | DEVICE ID Confidence: " + device_info[4] + " | DEV EUI Confidence: " + device_info[5] + " | APP EUI Confidence: " + device_info[6] + " | APP KEY Confidence: " + device_info[7])
                # Suppression de l'image capturée après traitement
                if os.path.exists(image_path + f'DEV-{device_info[0]}.jpg'):
                    os.remove(image_path + f'DEV-{device_info[0]}.jpg')
                # Renommage de l'image capturée après traitement avec l'ID écrit à la main sur la boîte
                os.rename(image_path + image_filename, image_path + f'DEV-{device_info[0]}.jpg') 
            except Exception as e:
                print(f'Erreur: {e}')
            i += 1
        elif key & 0xFF == ord('q'):
            break

    # Libération de la capture vidéo et fermeture des fenêtres
    cap.release()
    cv2.destroyAllWindows()


# Demande à l'utilisateur de saisir l'index de la caméra
while True:
    index_camera = input("Entrez le numéro d'index de votre caméra, en général 0 correspond à la caméra intégrée de votre ordinateur, et 1 à la caméra externe (index compris entre 0 et 9): ")
    
    if index_camera.isdigit():
        if 0 <= int(index_camera) <= 9:
            index_camera = int(index_camera)
            break
        else:
            print("Veuillez entrer un numéro d'index entre 0 et 9.")
    else:
        print("Veuillez entrer uniquement des chiffres.")

# Création du fichier CSV s'il n'existe pas
if not os.path.isfile('extracted_data.csv'):
    with open('extracted_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['DEVICE_ID', 'DEV_EUI', 'APP_EUI', 'APP_KEY', 'DEVICE_ID_CONFIDENCE', 'DEV_EUI_CONFIDENCE', 'APP_EUI_CONFIDENCE', 'APP_KEY_CONFIDENCE'])

# Appel de la fonction pour ouvrir la caméra et traiter les images
open_camera(index_camera)