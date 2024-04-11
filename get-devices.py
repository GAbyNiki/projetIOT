import os
import requests
import csv
import pandas as pd

# Lecture des données du fichier 'informations.csv'
info_df = pd.read_csv('informations.csv', index_col=0)

# Récupérer les valeurs des informations dans 'informations.csv'
server_ip = info_df.loc['SERVER_IP', info_df.columns[0]]
bearer = info_df.loc['BEARER', info_df.columns[0]]
application_id = info_df.loc['APP_ID', info_df.columns[0]]

# Adresse du network server avec l'adresse IP récupérée
url = f'http://{server_ip}:8090/api/devices'

params = {
    'applicationId': f'{application_id}',
    'limit': 700
}

# Headers avec le Bearer
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {bearer}',
}

# Envoyer une requête GET pour récupérer les devices
current_directory = os.path.dirname(os.path.abspath(__file__))
response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    devices = response.json()['result']  # Accéder aux résultats

    # Chemin complet pour le fichier CSV pour l'enregistrer dans le même répertoire que celui du script
    csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'devices.csv')

    # Écrire les données dans un fichier CSV
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=devices[0].keys())
        writer.writeheader()
        for device in devices:
            writer.writerow(device)
    print("Fichier CSV créé avec succès.")
else:
    print("Erreur lors de la récupération des devices:", response.status_code)
    print("Réponse de l'API:", response.json())
