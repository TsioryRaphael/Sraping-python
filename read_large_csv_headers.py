import csv
import os

CSV_FOLDER = './entreprises'

# Liste des fichiers volumineux à lire
large_files = ['Entreprise.csv', 'Nom.csv']

for filename in large_files:
    path = os.path.join(CSV_FOLDER, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            print(f"Colonnes de {filename} :")
            print(header)
    else:
        print(f"Fichier {filename} introuvable.")
