# import os
# import pandas as pd
# import mysql.connector
# from mysql.connector import errorcode

# # Configuration de la connexion MySQL

# MYSQL_CONFIG = {
#     'user': 'root',         # À adapter
#     'password': '', # À adapter
#     'host': 'localhost',
#     'database': 'registre_entreprise_quebec', # À adapter
#     'raise_on_warnings': True
# }

# # Dictionnaire de structure des tables et clés étrangères
# TABLES = {
#     'Entreprise': (
#         '''
#         CREATE TABLE IF NOT EXISTS Entreprise (
#             NEQ VARCHAR(20) PRIMARY KEY,
#             IND_FAIL VARCHAR(10),
#             DAT_IMMAT VARCHAR(20),
#             COD_REGIM_JURI VARCHAR(20),
#             COD_INTVAL_EMPLO_QUE VARCHAR(20),
#             DAT_CESS_PREVU VARCHAR(20),
#             COD_STAT_IMMAT VARCHAR(20),
#             COD_FORME_JURI VARCHAR(20),
#             DAT_STAT_IMMAT VARCHAR(20),
#             COD_REGIM_JURI_CONSTI VARCHAR(20),
#             DAT_DEPO_DECLR VARCHAR(20),
#             AN_DECL VARCHAR(10),
#             AN_PROD VARCHAR(10),
#             DAT_LIMIT_PROD VARCHAR(20),
#             AN_PROD_PRE VARCHAR(10),
#             DAT_LIMIT_PROD_PRE VARCHAR(20),
#             DAT_MAJ_INDEX_NOM VARCHAR(20),
#             COD_ACT_ECON_CAE VARCHAR(20),
#             NO_ACT_ECON_ASSUJ VARCHAR(20),
#             DESC_ACT_ECON_ASSUJ TEXT,
#             COD_ACT_ECON_CAE2 VARCHAR(20),
#             NO_ACT_ECON_ASSUJ2 VARCHAR(20),
#             DESC_ACT_ECON_ASSUJ2 TEXT,
#             NOM_LOCLT_CONSTI TEXT,
#             DAT_CONSTI VARCHAR(20),
#             IND_CONVEN_UNMN_ACTNR VARCHAR(10),
#             IND_RET_TOUT_POUVR VARCHAR(10),
#             IND_LIMIT_RESP VARCHAR(10),
#             DAT_DEB_RESP VARCHAR(20),
#             DAT_FIN_RESP VARCHAR(20),
#             OBJET_SOC TEXT,
#             NO_MTR_VOLONT VARCHAR(20),
#             ADR_DOMCL_ADR_DISP VARCHAR(20),
#             ADR_DOMCL_LIGN1_ADR TEXT,
#             ADR_DOMCL_LIGN2_ADR TEXT,
#             ADR_DOMCL_LIGN3_ADR TEXT,
#             ADR_DOMCL_LIGN4_ADR TEXT
#         ) ENGINE=InnoDB;
#         '''
#     ),
#     'Nom': (
#         '''
#         CREATE TABLE IF NOT EXISTS Nom (
#             NEQ VARCHAR(20),
#             NOM_ASSUJ TEXT,
#             NOM_ASSUJ_LANG_ETRNG TEXT,
#             STAT_NOM VARCHAR(10),
#             TYP_NOM_ASSUJ VARCHAR(10),
#             DAT_INIT_NOM_ASSUJ VARCHAR(20),
#             DAT_FIN_NOM_ASSUJ VARCHAR(20),
#             FOREIGN KEY (NEQ) REFERENCES Entreprise(NEQ)
#         ) ENGINE=InnoDB;
#         '''
#     ),
#     'Etablissements': (
#         '''
#         CREATE TABLE IF NOT EXISTS Etablissements (
#             NEQ VARCHAR(20),
#             NO_SUF_ETAB VARCHAR(10),
#             IND_ETAB_PRINC VARCHAR(5),
#             IND_SALON_BRONZ VARCHAR(5),
#             IND_VENTE_TABAC_DETL VARCHAR(5),
#             IND_DISP VARCHAR(5),
#             LIGN1_ADR TEXT,
#             LIGN2_ADR TEXT,
#             LIGN3_ADR TEXT,
#             LIGN4_ADR TEXT,
#             COD_ACT_ECON VARCHAR(10),
#             DESC_ACT_ECON_ETAB TEXT,
#             NO_ACT_ECON_ETAB VARCHAR(10),
#             COD_ACT_ECON2 VARCHAR(10),
#             DESC_ACT_ECON_ETAB2 TEXT,
#             NO_ACT_ECON_ETAB2 VARCHAR(10),
#             NOM_ETAB TEXT,
#             FOREIGN KEY (NEQ) REFERENCES Entreprise(NEQ)
#         ) ENGINE=InnoDB;
#         '''
#     ),
#     'FusionScissions': (
#         '''
#         CREATE TABLE IF NOT EXISTS FusionScissions (
#             NEQ VARCHAR(20),
#             NEQ_ASSUJ_REL VARCHAR(20),
#             DENOMN_SOC TEXT,
#             COD_RELA_ASSUJ VARCHAR(10),
#             DAT_EFCTVT VARCHAR(20),
#             IND_DISP VARCHAR(5),
#             LIGN1_ADR TEXT,
#             LIGN2_ADR TEXT,
#             LIGN3_ADR TEXT,
#             LIGN4_ADR TEXT,
#             FOREIGN KEY (NEQ) REFERENCES Entreprise(NEQ)
#         ) ENGINE=InnoDB;
#         '''
#     ),
#     'ContinuationsTransformations': (
#         '''
#         CREATE TABLE IF NOT EXISTS ContinuationsTransformations (
#             NEQ VARCHAR(20),
#             COD_TYP_CHANG VARCHAR(10),
#             COD_REGIM_JURI VARCHAR(10),
#             AUTR_REGIM_JURI TEXT,
#             NOM_LOCLT TEXT,
#             DAT_EFCTVT VARCHAR(20),
#             FOREIGN KEY (NEQ) REFERENCES Entreprise(NEQ)
#         ) ENGINE=InnoDB;
#         '''
#     ),
#     'DomaineValeur': (
#         '''
#         CREATE TABLE IF NOT EXISTS DomaineValeur (
#             TYP_DOM_VAL VARCHAR(20),
#             COD_DOM_VAL VARCHAR(20),
#             VAL_DOM_FRAN TEXT
#         ) ENGINE=InnoDB;
#         '''
#     ),
# }

# CSV_FOLDER = './entreprises'


# def connect_mysql():
#     try:
#         cnx = mysql.connector.connect(**MYSQL_CONFIG)
#         return cnx
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Erreur d'identification MySQL")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("La base de données n'existe pas")
#         else:
#             print(err)
#         return None

# def create_tables(cursor):
#     for name, ddl in TABLES.items():
#         try:
#             print(f"Création de la table {name}...")
#             cursor.execute(ddl)
#         except mysql.connector.Error as err:
#             print(f"Erreur lors de la création de {name}: {err}")

# def insert_data(cursor, table, df):
#     import numpy as np
#     cols = ','.join(df.columns)
#     placeholders = ','.join(['%s'] * len(df.columns))
#     sql = f"INSERT IGNORE INTO {table} ({cols}) VALUES ({placeholders})"
#     for row in df.itertuples(index=False, name=None):
#         # Remplace les NaN par None
#         row_clean = tuple(None if (x is np.nan or x != x) else x for x in row)
#         try:
#             cursor.execute(sql, row_clean)
#         except Exception as e:
#             print(f"Erreur insertion dans {table}: {e} | Ligne: {row_clean}")


# def main():
#     cnx = connect_mysql()
#     if cnx is None:
#         return
#     cursor = cnx.cursor()

#     # create_tables(cursor)
#     cnx.commit()

#     # Traite Entreprise.csv en priorité
#     # --- Spécifier ici les fichiers à importer ---
#     files_to_import = [
#         'Entreprise.csv',
#         'Etablissements.csv',
#         'Nom.csv',
#         'FusionScissions.csv',
#     ]

#     # --- Ancien code pour parcourir tous les fichiers automatiquement ---
#     # all_files = [f for f in os.listdir(CSV_FOLDER) if f.endswith('.csv')]
#     # files_ordered = []
#     # if 'Entreprise.csv' in all_files:
#     #     files_ordered.append('Entreprise.csv')
#     # files_ordered += [f for f in all_files if f != 'Entreprise.csv']

#     for filename in files_to_import:
#         table = os.path.splitext(filename)[0]
#         if table not in TABLES:
#             print(f"Aucune table définie pour {table}, fichier ignoré.")
#             continue
#         print(f"Import de {filename} dans {table} à partir de la ligne 100000...")
#         # Lecture robuste : gestion des séparateurs et des champs avec virgules
#         try:
#             df = pd.read_csv(
#                 os.path.join(CSV_FOLDER, filename),
#                 dtype=str,
#                 sep=',',
#                 quotechar='"',
#                 encoding='utf-8',
#                 engine='python',
#                 skipinitialspace=True,
#                 # skiprows=range(1, 100000)  # saute les 99999 premières lignes de données (garde l'en-tête)
#             )
#             # Nettoyage éventuel des colonnes (ex: BOM)
#             df.columns = [col.lstrip('\ufeff') for col in df.columns]
#         except Exception as e:
#             print(f"Erreur lecture {filename}: {e}")
#             continue
#         insert_data(cursor, table, df)
#         cnx.commit()
#     cursor.close()
#     cnx.close()
#     print("Import terminé.")

# if __name__ == '__main__':
#     main()

# import os
# import pandas as pd
# import mysql.connector
# from mysql.connector import errorcode

# # Configuration de la connexion MySQL
# MYSQL_CONFIG = {
#     'user': 'root',         # À adapter
#     'password': '', # À adapter
#     'host': 'localhost',
#     'database': 'registre_entreprise_quebec', # À adapter
#     'raise_on_warnings': True
# }

# # Dictionnaire de structure des tables et clés étrangères
# TABLES = {
#     'Etablissements': (
#         '''
#         CREATE TABLE IF NOT EXISTS Etablissements (
#             NEQ VARCHAR(10),
#             NO_SUF_ETAB INT,
#             IND_ETAB_PRINC CHAR(1),
#             IND_SALON_BRONZ CHAR(1),
#             IND_VENTE_TABAC_DETL CHAR(1),
#             IND_DISP CHAR(1),
#             LIGN1_ADR VARCHAR(100),
#             LIGN2_ADR VARCHAR(100),
#             LIGN3_ADR VARCHAR(100),
#             LIGN4_ADR VARCHAR(100),
#             COD_ACT_ECON VARCHAR(15),
#             DESC_ACT_ECON_ETAB VARCHAR(250),
#             NO_ACT_ECON_ETAB INT,
#             COD_ACT_ECON2 VARCHAR(15),
#             DESC_ACT_ECON_ETAB2 VARCHAR(250),
#             NO_ACT_ECON_ETAB2 INT,
#             NOM_ETAB VARCHAR(500),
#             FOREIGN KEY (NEQ) REFERENCES Entreprise(NEQ)
#         ) ENGINE=InnoDB;
#         '''
#     ),
#     'FusionScissions': (
#         '''
#         CREATE TABLE IF NOT EXISTS FusionScissions (
#             NEQ VARCHAR(10),
#             NEQ_ASSUJ_REL VARCHAR(10),
#             DENOMN_SOC VARCHAR(500),
#             COD_RELA_ASSUJ VARCHAR(15),
#             DAT_EFCTVT DATETIME,
#             IND_DISP CHAR(1),
#             LIGN1_ADR VARCHAR(100),
#             LIGN2_ADR VARCHAR(100),
#             LIGN3_ADR VARCHAR(100),
#             LIGN4_ADR VARCHAR(100),
#             FOREIGN KEY (NEQ) REFERENCES Entreprise(NEQ)
#         ) ENGINE=InnoDB;
#         '''
#     ),
#     'ContinuationsTransformations': (
#         '''
#         CREATE TABLE IF NOT EXISTS ContinuationsTransformations (
#             NEQ VARCHAR(10),
#             COD_TYP_CHANG VARCHAR(10),
#             COD_REGIM_JURI VARCHAR(15),
#             AUTR_REGIM_JURI VARCHAR(100),
#             NOM_LOCLT VARCHAR(60),
#             DAT_EFCTVT DATETIME,
#             FOREIGN KEY (NEQ) REFERENCES Entreprise(NEQ)
#         ) ENGINE=InnoDB;
#         '''
#     ),
#     'DomaineValeur': (
#         '''
#         CREATE TABLE IF NOT EXISTS DomaineValeur (
#             TYP_DOM_VAL VARCHAR(50),
#             COD_DOM_VAL VARCHAR(15),
#             VAL_DOM_FRAN VARCHAR(250),
#             PRIMARY KEY (TYP_DOM_VAL, COD_DOM_VAL)
#         ) ENGINE=InnoDB;
#         '''
#     ),
# }

# CSV_FOLDER = './entreprises'

# def connect_mysql():
#     try:
#         cnx = mysql.connector.connect(**MYSQL_CONFIG)
#         return cnx
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Erreur d'identification MySQL")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("La base de données n'existe pas")
#         else:
#             print(err)
#         return None

# def create_tables(cursor):
#     for name, ddl in TABLES.items():
#         try:
#             print(f"Création de la table {name}...")
#             cursor.execute(ddl)
#         except mysql.connector.Error as err:
#             print(f"Erreur lors de la création de {name}: {err}")

# def insert_data(cursor, table, df):
#     import numpy as np
#     cols = ','.join(df.columns)
#     placeholders = ','.join(['%s'] * len(df.columns))
#     sql = f"INSERT IGNORE INTO {table} ({cols}) VALUES ({placeholders})"
#     for row in df.itertuples(index=False, name=None):
#         # Remplace les NaN par None
#         row_clean = tuple(None if (x is np.nan or x != x) else x for x in row)
#         try:
#             cursor.execute(sql, row_clean)
#         except Exception as e:
#             print(f"Erreur insertion dans {table}: {e} | Ligne: {row_clean}")

# def main():
#     cnx = connect_mysql()
#     if cnx is None:
#         return
#     cursor = cnx.cursor()

#     create_tables(cursor)
#     cnx.commit()

#     # Importe tous les CSVs du dossier, en priorisant Entreprise.csv en raison des FK
#     all_files = [f for f in os.listdir(CSV_FOLDER) if f.endswith('.csv')]
#     files_ordered = []
#     if 'Entreprise.csv' in all_files:
#         files_ordered.append('Entreprise.csv')
#     files_ordered += [f for f in all_files if f != 'Entreprise.csv']

#     for filename in files_ordered:
#         table = os.path.splitext(filename)[0]
#         if table not in TABLES:
#             print(f"Aucune table définie pour {table}, fichier ignoré.")
#             continue
#         print(f"Import de {filename} dans {table}...")
#         # Lecture robuste : gestion des séparateurs et des champs avec virgules
#         # Parse les dates automatiquement avec heure
#         try:
#             df = pd.read_csv(
#                 os.path.join(CSV_FOLDER, filename),
#                 dtype=str,
#                 sep=',',
#                 quotechar='"',
#                 encoding='utf-8',
#                 engine='python',
#                 skipinitialspace=True,
#                 parse_dates=True,
#                 date_format='%Y-%m-%d %H:%M:%S'  # Format datetime avec heure
#             )
#             # Nettoyage éventuel des colonnes (ex: BOM)
#             df.columns = [col.lstrip('\ufeff') for col in df.columns]
#         except Exception as e:
#             print(f"Erreur lecture {filename}: {e}")
#             continue
#         insert_data(cursor, table, df)
#         cnx.commit()
#     cursor.close()
#     cnx.close()
#     print("Import terminé.")

# if __name__ == '__main__':
#     main()

# import os
# import pandas as pd
# import mysql.connector
# from mysql.connector import errorcode

# # Configuration de la connexion MySQL
# MYSQL_CONFIG = {
#     'user': 'root',         # À adapter
#     'password': '',         # À adapter
#     'host': 'localhost',
#     'database': 'registre_entreprise_quebec', # À adapter
#     'raise_on_warnings': True
# }

# # Dictionnaire de structure des tables et clés étrangères
# TABLES = {
#     'Entreprise': (
#         '''
#         CREATE TABLE IF NOT EXISTS Entreprise (
#             NEQ VARCHAR(10) PRIMARY KEY,
#             IND_FAIL CHAR(1),
#             DAT_IMMAT DATETIME,
#             COD_REGIM_JURI VARCHAR(15),
#             COD_INTVAL_EMPLO_QUE VARCHAR(15),
#             DAT_CESS_PREVU DATETIME,
#             COD_STAT_IMMAT VARCHAR(15),
#             COD_FORME_JURI VARCHAR(15),
#             DAT_STAT_IMMAT DATETIME,
#             COD_REGIM_JURI_CONSTI VARCHAR(15),
#             DAT_DEPO_DECLR DATETIME,
#             AN_DECL INT,
#             AN_PROD INT,
#             DAT_LIMIT_PROD DATETIME,
#             AN_PROD_PRE INT,
#             DAT_LIMIT_PROD_PRE DATETIME,
#             DAT_MAJ_INDEX_NOM DATETIME,
#             COD_ACT_ECON_CAE VARCHAR(15),
#             NO_ACT_ECON_ASSUJ INT,
#             DESC_ACT_ECON_ASSUJ VARCHAR(250),
#             COD_ACT_ECON_CAE2 VARCHAR(15),
#             NO_ACT_ECON_ASSUJ2 INT,
#             DESC_ACT_ECON_ASSUJ2 VARCHAR(250),
#             NOM_LOCLT_CONSTI VARCHAR(60),
#             DAT_CONSTI DATETIME,
#             IND_CONVEN_UNMN_ACTNR CHAR(1),
#             IND_RET_TOUT_POUVR CHAR(1),
#             IND_LIMIT_RESP CHAR(1),
#             DAT_DEB_RESP DATETIME,
#             DAT_FIN_RESP DATETIME,
#             OBJET_SOC VARCHAR(1000),
#             NO_MTR_VOLONT VARCHAR(10),
#             ADR_DOMCL_ADR_DISP CHAR(1),
#             ADR_DOMCL_LIGN1_ADR VARCHAR(100),
#             ADR_DOMCL_LIGN2_ADR VARCHAR(100),
#             ADR_DOMCL_LIGN3_ADR VARCHAR(100),
#             ADR_DOMCL_LIGN4_ADR VARCHAR(100)
#         ) ENGINE=InnoDB;
#         '''
#     ),
#     'Nom': (
#         '''
#         CREATE TABLE IF NOT EXISTS Nom (
#             NEQ VARCHAR(10),
#             NOM_ASSUJ VARCHAR(500),
#             NOM_ASSUJ_LANG_ETRNG VARCHAR(500),
#             STAT_NOM VARCHAR(15),
#             TYP_NOM_ASSUJ VARCHAR(15),
#             DAT_INIT_NOM_ASSUJ DATETIME,
#             DAT_FIN_NOM_ASSUJ DATETIME,
#             FOREIGN KEY (NEQ) REFERENCES Entreprise(NEQ)
#         ) ENGINE=InnoDB;
#         '''
#     ),
#     'Etablissement': (
#         '''
#         CREATE TABLE IF NOT EXISTS Etablissements (
#             NEQ VARCHAR(10),
#             NO_SUF_ETAB INT,
#             IND_ETAB_PRINC CHAR(1),
#             IND_SALON_BRONZ CHAR(1),
#             IND_VENTE_TABAC_DETL CHAR(1),
#             IND_DISP CHAR(1),
#             LIGN1_ADR VARCHAR(100),
#             LIGN2_ADR VARCHAR(100),
#             LIGN3_ADR VARCHAR(100),
#             LIGN4_ADR VARCHAR(100),
#             COD_ACT_ECON VARCHAR(15),
#             DESC_ACT_ECON_ETAB VARCHAR(250),
#             NO_ACT_ECON_ETAB INT,
#             COD_ACT_ECON2 VARCHAR(15),
#             DESC_ACT_ECON_ETAB2 VARCHAR(250),
#             NO_ACT_ECON_ETAB2 INT,
#             NOM_ETAB VARCHAR(500),
#             FOREIGN KEY (NEQ) REFERENCES Entreprise(NEQ)
#         ) ENGINE=InnoDB;
#         '''
#     ),
#     'FusionScission': (
#         '''
#         CREATE TABLE IF NOT EXISTS FusionScissions (
#             NEQ VARCHAR(10),
#             NEQ_ASSUJ_REL VARCHAR(10),
#             DENOMN_SOC VARCHAR(500),
#             COD_RELA_ASSUJ VARCHAR(15),
#             DAT_EFCTVT DATETIME,
#             IND_DISP CHAR(1),
#             LIGN1_ADR VARCHAR(100),
#             LIGN2_ADR VARCHAR(100),
#             LIGN3_ADR VARCHAR(100),
#             LIGN4_ADR VARCHAR(100),
#             FOREIGN KEY (NEQ) REFERENCES Entreprise(NEQ)
#         ) ENGINE=InnoDB;
#         '''
#     ),
#     'ContinuationTransformation': (
#         '''
#         CREATE TABLE IF NOT EXISTS ContinuationsTransformations (
#             NEQ VARCHAR(10),
#             COD_TYP_CHANG VARCHAR(10),
#             COD_REGIM_JURI VARCHAR(15),
#             AUTR_REGIM_JURI VARCHAR(100),
#             NOM_LOCLT VARCHAR(60),
#             DAT_EFCTVT DATETIME,
#             FOREIGN KEY (NEQ) REFERENCES Entreprise(NEQ)
#         ) ENGINE=InnoDB;
#         '''
#     ),
#     'DomaineValeur': (
#         '''
#         CREATE TABLE IF NOT EXISTS DomaineValeur (
#             TYP_DOM_VAL VARCHAR(50),
#             COD_DOM_VAL VARCHAR(15),
#             VAL_DOM_FRAN VARCHAR(250),
#             PRIMARY KEY (TYP_DOM_VAL, COD_DOM_VAL)
#         ) ENGINE=InnoDB;
#         '''
#     ),
# }

# CSV_FOLDER = './entreprises'
# CSV_FILE = 'Nom.csv'  # Nom du fichier CSV défini en brut

# def connect_mysql():
#     try:
#         cnx = mysql.connector.connect(**MYSQL_CONFIG)
#         return cnx
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Erreur d'identification MySQL")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("La base de données n'existe pas")
#         else:
#             print(err)
#         return None

# def create_tables(cursor):
#     for name, ddl in TABLES.items():
#         try:
#             print(f"Création de la table {name}...")
#             cursor.execute(ddl)
#         except mysql.connector.Error as err:
#             print(f"Erreur lors de la création de {name}: {err}")

# def insert_data(cursor, table, df):
#     import numpy as np
#     cols = ','.join(df.columns)
#     placeholders = ','.join(['%s'] * len(df.columns))
#     sql = f"INSERT IGNORE INTO {table} ({cols}) VALUES ({placeholders})"
#     for row in df.itertuples(index=False, name=None):
#         # Remplace les NaN par None
#         row_clean = tuple(None if (x is np.nan or x != x) else x for x in row)
#         try:
#             cursor.execute(sql, row_clean)
#         except Exception as e:
#             print(f"Erreur insertion dans {table}: {e} | Ligne: {row_clean}")

# def main():
#     # Vérifie si le fichier existe
#     if not os.path.exists(os.path.join(CSV_FOLDER, CSV_FILE)):
#         print(f"Le fichier {CSV_FILE} n'existe pas dans {CSV_FOLDER}.")
#         return

#     # Connexion à MySQL
#     cnx = connect_mysql()
#     if cnx is None:
#         return
#     cursor = cnx.cursor()

#     # Création des tables
#     create_tables(cursor)
#     cnx.commit()

#     # Extraction du nom de la table à partir du nom du fichier
#     table = os.path.splitext(CSV_FILE)[0]
#     if table not in TABLES:
#         print(f"Aucune table définie pour {table}, fichier ignoré.")
#         cursor.close()
#         cnx.close()
#         return

#     print(f"Import de {CSV_FILE} dans {table}...")
#     # Lecture robuste : gestion des séparateurs et des champs avec virgules
#     try:
#         df = pd.read_csv(
#             os.path.join(CSV_FOLDER, CSV_FILE),
#             dtype=str,
#             sep=',',
#             quotechar='"',
#             encoding='utf-8',
#             engine='python',
#             skipinitialspace=True,
#             parse_dates=True,
#             date_format='%Y-%m-%d %H:%M:%S'  # Format datetime avec heure
#         )
#         # Nettoyage éventuel des colonnes (ex: BOM)
#         df.columns = [col.lstrip('\ufeff') for col in df.columns]
#     except Exception as e:
#         print(f"Erreur lecture {CSV_FILE}: {e}")
#         cursor.close()
#         cnx.close()
#         return

#     # Insertion des données
#     insert_data(cursor, table, df)
#     cnx.commit()

#     cursor.close()
#     cnx.close()
#     print(f"Import de {CSV_FILE} terminé.")

# if __name__ == '__main__':
#     main()

# import os
# import pandas as pd
# import mysql.connector
# from mysql.connector import errorcode

# # Configuration de la connexion MySQL
# MYSQL_CONFIG = {
#     'user': 'root',         
#     'password': '',        
#     'host': 'localhost',
#     'database': 'registre_entreprise_quebec', 
#     'raise_on_warnings': True
# }

# # Dictionnaire de structure des tables
# TABLES = {
#     'Administrateur': (
#         '''
#         CREATE TABLE IF NOT EXISTS Administrateur (
#             NEQ VARCHAR(10),
#             Nom VARCHAR(100),
#             Prénom VARCHAR(100),
#             Adresse VARCHAR(255),
#             Fonction VARCHAR(100) DEFAULT 'Actionnaire',  -- Default value for NULL
#             FOREIGN KEY (NEQ) REFERENCES Entreprise(NEQ)
#         ) ENGINE=InnoDB;
#         '''
#     ),
# }

# CSV_FOLDER = './entreprises'
# CSV_FILE = 'Administrateurs.csv'  # Nom du fichier CSV

# def connect_mysql():
#     try:
#         cnx = mysql.connector.connect(**MYSQL_CONFIG)
#         return cnx
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Erreur d'identification MySQL")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("La base de données n'existe pas")
#         else:
#             print(err)
#         return None

# def create_tables(cursor):
#     for name, ddl in TABLES.items():
#         try:
#             print(f"Création de la table {name}...")
#             cursor.execute(ddl)
#         except mysql.connector.Error as err:
#             print(f"Erreur lors de la création de {name}: {err}")

# def insert_data(cursor, table, df):
#     import numpy as np
#     cols = ','.join(df.columns)
#     placeholders = ','.join(['%s'] * len(df.columns))
#     sql = f"INSERT IGNORE INTO {table} ({cols}) VALUES ({placeholders})"
#     for row in df.itertuples(index=False, name=None):
#         # Remplace les NaN, empty strings, or whitespace-only strings by None
#         row_clean = tuple(None if (x is np.nan or x != x or str(x).strip() == '') else x for x in row)
#         # Debug: Print rows where Fonction is None
#         fonction_index = df.columns.get_loc('Fonction')
#         if row_clean[fonction_index] is None:
#             print(f"Row with empty/NULL Fonction: {row_clean}")
#         try:
#             cursor.execute(sql, row_clean)
#         except mysql.connector.Error as e:
#             print(f"Erreur insertion dans {table}: {e} | Ligne: {row_clean}")

# def main():
#     # Vérifie si le fichier existe
#     if not os.path.exists(os.path.join(CSV_FOLDER, CSV_FILE)):
#         print(f"Le fichier {CSV_FILE} n'existe pas dans {CSV_FOLDER}.")
#         return

#     # Connexion à MySQL
#     cnx = connect_mysql()
#     if cnx is None:
#         return
#     cursor = cnx.cursor()

#     # Création des tables
#     # create_tables(cursor)
#     # cnx.commit()

#     # Extraction du nom de la table
#     table = 'Administrateur'
#     if table not in TABLES:
#         print(f"Aucune table définie pour {table}, fichier ignoré.")
#         cursor.close()
#         cnx.close()
#         return

#     print(f"Import de {CSV_FILE} dans {table}...")
#     # Lecture robuste : gestion des séparateurs et des champs avec virgules
#     try:
#         df = pd.read_csv(
#             os.path.join(CSV_FOLDER, CSV_FILE),
#             dtype=str,
#             sep=',',
#             quotechar='"',
#             encoding='utf-8',
#             engine='python',
#             skipinitialspace=True,
#             na_values=['', ' ', 'NaN']  # Treat empty strings and whitespace as NaN
#         )
#         # Nettoyage éventuel des colonnes (ex: BOM)
#         df.columns = [col.lstrip('\ufeff') for col in df.columns]
#         # Debug: Print number of rows with empty Fonction
#         empty_fonction_count = df['Fonction'].isna().sum()
#         print(f"Nombre de lignes avec Fonction vide/NULL dans le CSV: {empty_fonction_count}")
#     except Exception as e:
#         print(f"Erreur lecture {CSV_FILE}: {e}")
#         cursor.close()
#         cnx.close()
#         return

#     # Insertion des données
#     insert_data(cursor, table, df)
#     cnx.commit()


#     cursor.close()
#     cnx.close()
#     print(f"Import de {CSV_FILE} terminé.")

# if __name__ == '__main__':
#     main()

import os
import pandas as pd
import mysql.connector
from mysql.connector import errorcode

# Configuration de la connexion MySQL
MYSQL_CONFIG = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'licencerbq',
    'raise_on_warnings': True
}

# Dictionnaire de structure des tables
TABLES = {
    'LicenceRBQ': (
        '''
        CREATE TABLE IF NOT EXISTS LicenceRBQ (
            id INT AUTO_INCREMENT PRIMARY KEY,
            numero_licence VARCHAR(20),
            statut_licence VARCHAR(50),
            type_licence VARCHAR(50),
            date_delivrance DATE,
            restriction VARCHAR(3),
            date_debut_restriction DATE,
            date_fin_restriction DATE,
            association_cautionnement VARCHAR(255),
            montant_caution DECIMAL(15,2),
            date_paiement_annuel DATE,
            mandataire VARCHAR(50),
            courriel VARCHAR(100),
            adresse TEXT,
            NEQ VARCHAR(10),
            nom_intervenant VARCHAR(255),
            numero_telephone VARCHAR(20),
            municipalite VARCHAR(100),
            statut_juridique VARCHAR(100),
            code_region_admin VARCHAR(10),
            region_admin VARCHAR(100),
            nombre_sous_categories INT,
            categories TEXT,
            sous_categories TEXT,
            autre_nom TEXT
        ) ENGINE=InnoDB;
        '''
    ),
}

EXCEL_FOLDER = './entreprises'
EXCEL_FILE = 'Licence.xlsx'  

def connect_mysql():
    try:
        cnx = mysql.connector.connect(**MYSQL_CONFIG)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erreur d'identification MySQL")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de données n'existe pas")
        else:
            print(err)
        return None

def create_tables(cursor):
    for name, ddl in TABLES.items():
        try:
            print(f"Création de la table {name}...")
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            print(f"Erreur lors de la création de {name}: {err}")

def insert_data(cursor, table, df):
    import numpy as np
    # Define expected columns (excluding id)
    expected_columns = ['numero_licence', 'statut_licence', 'type_licence', 'date_delivrance',
                       'restriction', 'date_debut_restriction', 'date_fin_restriction',
                       'association_cautionnement', 'montant_caution', 'date_paiement_annuel',
                       'mandataire', 'courriel', 'adresse', 'NEQ', 'nom_intervenant',
                       'numero_telephone', 'municipalite', 'statut_juridique',
                       'code_region_admin', 'region_admin', 'nombre_sous_categories',
                       'categories', 'sous_categories', 'autre_nom']
    # Use the renamed columns from the DataFrame
    columns = [col for col in df.columns if col in expected_columns]
    if not columns:
        print("Aucune colonne valide trouvée pour l'insertion.")
        return
    cols = ','.join(columns)
    placeholders = ','.join(['%s'] * len(columns))
    sql = f"INSERT IGNORE INTO {table} ({cols}) VALUES ({placeholders})"
    for row in df[columns].itertuples(index=False, name=None):  # Use only the valid columns
        # Remplace les NaN, empty strings, or whitespace-only strings by None
        row_clean = tuple(None if (x is np.nan or x != x or str(x).strip() == '') else x for x in row)
        try:
            cursor.execute(sql, row_clean)
        except mysql.connector.Error as e:
            print(f"Erreur insertion dans {table}: {e} | Ligne: {row_clean}")

def main():
    # Vérifie si le fichier existe
    if not os.path.exists(os.path.join(EXCEL_FOLDER, EXCEL_FILE)):
        print(f"Le fichier {EXCEL_FILE} n'existe pas dans {EXCEL_FOLDER}.")
        return

    # Connexion à MySQL
    cnx = connect_mysql()
    if cnx is None:
        return
    cursor = cnx.cursor()

    # Création des tables
    create_tables(cursor)
    cnx.commit()

    # Extraction du nom de la table
    table = 'LicenceRBQ'
    if table not in TABLES:
        print(f"Aucune table définie pour {table}, fichier ignoré.")
        cursor.close()
        cnx.close()
        return

    print(f"Import de {EXCEL_FILE} dans {table}...")
    # Lecture robuste depuis Excel
    try:
        df = pd.read_excel(
            os.path.join(EXCEL_FOLDER, EXCEL_FILE),
            dtype=str,
            engine='openpyxl'
        )
        # Nettoyage éventuel des colonnes (ex: BOM)
        df.columns = [col.lstrip('\ufeff') for col in df.columns]
        
        # Renommez les colonnes du fichier Excel pour correspondre au schéma de la table
        df = df.rename(columns={
            'Numéro de licence': 'numero_licence',
            'Statut de la licence': 'statut_licence',
            'Type de licence': 'type_licence',
            'Date de délivrance': 'date_delivrance',
            'Restriction': 'restriction',
            'Date de début de la restriction': 'date_debut_restriction',
            'Date de fin de la restriction': 'date_fin_restriction',
            'Association ou compagnie fournissant le cautionnement': 'association_cautionnement',
            'Montant de la caution': 'montant_caution',
            'Date du paiement annuel': 'date_paiement_annuel',
            'Mandataire': 'mandataire',
            'Courriel': 'courriel',
            'Adresse': 'adresse',
            'NEQ': 'NEQ',
            'Nom de l\'intervenant': 'nom_intervenant',
            'Numéro de téléphone': 'numero_telephone',
            'Municipalité': 'municipalite',
            'Statut juridique': 'statut_juridique',
            'Code de région administrative': 'code_region_admin',
            'Région administrative': 'region_admin',
            'Nombre de sous-catégories autorisées': 'nombre_sous_categories',
            'Categorie': 'categories',
            'Sous-catégories': 'sous_categories',
            'Autre nom': 'autre_nom'
        })
        
        # Debug: Print DataFrame columns and first few rows to verify
        print("Colonnes du DataFrame après renommage:", df.columns.tolist())
        print("Premières lignes du DataFrame:", df.head().to_string())
    except Exception as e:
        print(f"Erreur lecture {EXCEL_FILE}: {e}")
        cursor.close()
        cnx.close()
        return

    # Insertion des données
    insert_data(cursor, table, df)
    cnx.commit()

    cursor.close()
    cnx.close()
    print(f"Import de {EXCEL_FILE} terminé.")

if __name__ == '__main__':
    main()

# import os
# import pandas as pd
# import mysql.connector
# from mysql.connector import errorcode

# # Configuration de la connexion MySQL
# MYSQL_CONFIG = {
#     'user': 'root',         
#     'password': '',        
#     'host': 'localhost',
#     'database': 'registre_entreprise_quebec', 
#     'raise_on_warnings': True
# }

# # Dictionnaire de structure des tables
# TABLES = {
#     'Etablissements': (
#         '''
#         CREATE TABLE IF NOT EXISTS Etablissement (
#             NEQ VARCHAR(10),
#             NO_SUF_ETAB VARCHAR(50),
#             IND_ETAB_PRINC VARCHAR(1),
#             IND_SALON_BRONZ VARCHAR(1),
#             IND_VENTE_TABAC_DETL VARCHAR(1),
#             IND_DISP VARCHAR(1),
#             LIGN1_ADR VARCHAR(255),
#             LIGN2_ADR VARCHAR(255),
#             LIGN3_ADR VARCHAR(255),
#             LIGN4_ADR VARCHAR(255),
#             COD_ACT_ECON VARCHAR(50),
#             DESC_ACT_ECON_ETAB TEXT,
#             NO_ACT_ECON_ETAB VARCHAR(50),
#             COD_ACT_ECON2 VARCHAR(50),
#             DESC_ACT_ECON_ETAB2 TEXT,
#             NO_ACT_ECON_ETAB2 VARCHAR(50),
#             FOREIGN KEY (NEQ) REFERENCES Entreprise(NEQ)
#         ) ENGINE=InnoDB;
#         '''
#     ),
# }

# CSV_FOLDER = './entreprises'
# CSV_FILE = 'Etablissements.csv'  # Nom du fichier CSV, ajustez si nécessaire (ex: minuscules)

# def connect_mysql():
#     try:
#         cnx = mysql.connector.connect(**MYSQL_CONFIG)
#         return cnx
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Erreur d'identification MySQL")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("La base de données n'existe pas")
#         else:
#             print(err)
#         return None

# def create_tables(cursor):
#     for name, ddl in TABLES.items():
#         try:
#             print(f"Création de la table {name}...")
#             cursor.execute(ddl)
#         except mysql.connector.Error as err:
#             print(f"Erreur lors de la création de {name}: {err}")

# def insert_data(cursor, table, df):
#     import numpy as np
#     cols = ','.join(df.columns)
#     placeholders = ','.join(['%s'] * len(df.columns))
#     sql = f"INSERT IGNORE INTO {table} ({cols}) VALUES ({placeholders})"
#     for row in df.itertuples(index=False, name=None):
#         # Remplace les NaN, empty strings, or whitespace-only strings by None
#         row_clean = tuple(None if (x is np.nan or x != x or str(x).strip() == '') else x for x in row)
#         try:
#             cursor.execute(sql, row_clean)
#         except mysql.connector.Error as e:
#             print(f"Erreur insertion dans {table}: {e} | Ligne: {row_clean}")

# def main():
#     # Vérifie si le fichier existe
#     if not os.path.exists(os.path.join(CSV_FOLDER, CSV_FILE)):
#         print(f"Le fichier {CSV_FILE} n'existe pas dans {CSV_FOLDER}.")
#         return

#     # Connexion à MySQL
#     cnx = connect_mysql()
#     if cnx is None:
#         return
#     cursor = cnx.cursor()

#     # Création des tables (décommentez si nécessaire)
#     # create_tables(cursor)
#     # cnx.commit()

#     # Extraction du nom de la table
#     table = 'Etablissements'
#     if table not in TABLES:
#         print(f"Aucune table définie pour {table}, fichier ignoré.")
#         cursor.close()
#         cnx.close()
#         return

#     print(f"Import de {CSV_FILE} dans {table}...")
#     # Lecture robuste : gestion des séparateurs et des champs avec virgules
#     try:
#         df = pd.read_csv(
#             os.path.join(CSV_FOLDER, CSV_FILE),
#             dtype=str,
#             sep=',',
#             quotechar='"',
#             encoding='utf-8',
#             engine='python',
#             skipinitialspace=True,
#             na_values=['', ' ', 'NaN']  # Treat empty strings and whitespace as NaN
#         )
#         # Nettoyage éventuel des colonnes (ex: BOM)
#         df.columns = [col.lstrip('\ufeff') for col in df.columns]
#     except Exception as e:
#         print(f"Erreur lecture {CSV_FILE}: {e}")
#         cursor.close()
#         cnx.close()
#         return

#     # Insertion des données
#     insert_data(cursor, table, df)
#     cnx.commit()

#     cursor.close()
#     cnx.close()
#     print(f"Import de {CSV_FILE} terminé.")

# if __name__ == '__main__':
#     main()