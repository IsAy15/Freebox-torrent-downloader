from methods import *
import sys
import os
import json
import requests

# On récupère les chemins des fichiers à ajouter à la liste d'attente de téléchargement
files_paths= sys.argv[1:]

if app_token == "" or main_url == "":
    print("La configuration (config.json) n'a pas été effectuée. Veuillez remplir les champs manquants dans le fichier.")

session_token=create_session(app_token)

for file_path in files_paths:

    file_path = str(file_path)

    upload_file(file_path, session_token)

logout(session_token)