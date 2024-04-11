import requests
import pandas as pd

# Lecture des données du fichier 'informations.csv'
info_df = pd.read_csv('informations.csv', index_col=0)

# Lecture des données du fichier 'extracted_data.csv'
data_df = pd.read_csv('extracted_data.csv')

# Récupérer les valeurs des informations dans 'informations.csv'
server_ip = info_df.loc['SERVER_IP', info_df.columns[0]]
bearer = info_df.loc['BEARER', info_df.columns[0]]
application_id = info_df.loc['APP_ID', info_df.columns[0]]
profile_id = info_df.loc['PROFILE_ID', info_df.columns[0]]

# Adresse du network server avec l'adresse IP récupérée
url = f'http://{server_ip}:8090/api/devices'

# Headers avec le Bearer
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {bearer}'
}

# Itérer sur les lignes des deux DataFrames
for index, data_row in data_df.iterrows():
    # Récupérer les valeurs des données dans 'extracted_data.csv'
    devEui = data_row['DEV_EUI']
    appEui = data_row['APP_EUI']
    appKey = data_row['APP_KEY']

    # Préparer les données de l'appareil
    data = {
        "device": {
            "applicationId": application_id,
            "devEui": devEui,
            "deviceProfileId": profile_id,
            "isDisabled": False,
            "name": devEui,
            "skipFcntCheck": True,
        }
    }

    # Envoyer la demande POST pour provisionner l'appareil
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"L'appareil avec devEui {devEui} a été provisionné avec succès.")
        print("Réponse de l'API:", response.json())
    else:
        print(f"Erreur lors de la provisionnement de l'appareil avec devEui {devEui}: {response.status_code}")
        print("Réponse de l'API:", response.json())
