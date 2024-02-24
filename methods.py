import hmac
import hashlib
import requests
import json
import os

# On récupère les informations de connexion à la Freebox depuis le fichier config.json
with open("config.json", 'r') as fichier:
     config = json.load(fichier)

main_url = config["domain"]

app_token = config["token"]


def get_challenge():
    url = main_url+"/api/v8/login/"

    challenge = requests.get(url).json()["result"]["challenge"]

    return challenge

def get_password(app_token):
    password = hmac.new(app_token.encode(), get_challenge().encode(), hashlib.sha1).hexdigest()
    return password

def create_session(app_token):

    url = main_url+"/api/v8/login/session/"

    payload = {
        "app_id": "anime_dl",
        "password": get_password(app_token)
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.json()["success"]:
        session_token = requests.post(url, headers=headers, data=json.dumps(payload)).json()["result"]["session_token"]
        print("Connexion à la Freebox réussie")
        return session_token
    else:
        print("Erreur : " + response.json())
        return False  

def logout(session_token):

    url = main_url+"/api/v8/login/logout/"

    payload = {}

    headers = {
        'Content-Type': 'application/json',
        'X-Fbx-App-Auth': session_token
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.json()["success"]:
        print("Déconnexion réussie")
    else:
        print("Erreur : " + response.json())

def upload_file(file_path, session_token):

    url = main_url+"/api/v8/downloads/add"

    headers = {"X-Fbx-App-Auth": session_token}

    file_name = os.path.basename(file_path)

    if file_path.endswith(".torrent") or file_path.endswith(".nzb"):

        with open(file_path, 'rb') as f:

            file = {'download_file': f}

            response = requests.post(url, headers=headers, files=file)

            if response.status_code == 200:

                print(file_name + " a bien été ajouté à la liste d'attente de téléchargement.")

            else:

                print("Erreur lors de l'ajout du fichier " + file_name + " : ", response.text)
    else:

        print("Un fichier " + file_path.split(".")[-1] + " ne peut pas être ajouté à la liste d'attente de téléchargement. Seuls les fichiers .torrent et .nzb sont acceptés.")