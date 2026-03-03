
import os
import pandas as pd
from itertools import combinations

# Répertoire contenant les fichiers Excel
directory = "./entreprises"

# Dictionnaire pour stocker les DataFrames
dataframes = {}
# Liste pour stocker les noms des colonnes de chaque fichier
columns_dict = {}
# Dictionnaire pour stocker les relations potentielles
relations = []

# Charger tous les fichiers Excel
for filename in os.listdir(directory):
    if filename.endswith(".xlsx"):
        file_path = os.path.join(directory, filename)
        df = pd.read_excel(file_path)
        dataframes[filename] = df
        columns_dict[filename] = set(df.columns)
        print(f"Chargé {filename} avec les colonnes : {list(df.columns)}")

# Trouver les colonnes communes entre les fichiers
print("\nColonnes communes entre les fichiers :")
for file1, file2 in combinations(dataframes.keys(), 2):
    common_columns = columns_dict[file1].intersection(columns_dict[file2])
    if common_columns:
        print(f"{file1} et {file2} partagent les colonnes : {common_columns}")
        for col in common_columns:
            # Vérifier si les valeurs dans les colonnes communes se correspondent
            values1 = set(dataframes[file1][col].dropna().astype(str))
            values2 = set(dataframes[file2][col].dropna().astype(str))
            common_values = values1.intersection(values2)
            if common_values:
                relations.append({
                    "fichiers": (file1, file2),
                    "colonne": col,
                    "valeurs_communes": len(common_values),
                    "exemple_valeurs": list(common_values)[:5]  # Limiter à 5 exemples
                })

# Afficher les relations trouvées
print("\nRelations potentielles basées sur les valeurs communes :")
if relations:
    for relation in relations:
        print(f"Fichiers : {relation['fichiers'][0]} et {relation['fichiers'][1]}")
        print(f"Colonne commune : {relation['colonne']}")
        print(f"Nombre de valeurs communes : {relation['valeurs_communes']}")
        print(f"Exemples de valeurs communes : {relation['exemple_valeurs']}\n")
else:
    print("Aucune relation trouvée basée sur les colonnes ou valeurs communes.")