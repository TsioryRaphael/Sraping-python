import requests
import zipfile
import io
import pandas as pd

def get_companies():
    # API CKAN pour obtenir le dataset du Registre des entreprises
    # dataset_id = "registre-des-entreprises"
    # base_url = "https://www.donneesquebec.ca/recherche/api/3/action"

    zip_url = "https://www.registreentreprises.gouv.qc.ca/RQAnonymeGR/GR/GR03/GR03A2_22A_PIU_RecupDonnPub_PC/FichierDonneesOuvertes.aspx"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    resp = requests.get(zip_url,headers=headers, allow_redirects=True, stream=True)
    
    print(f"Téléchargement du fichier ZIP depuis: {zip_url} ...")

    print(f"Code de statut de la réponse: {resp.status_code}")

    if not resp.content.startswith(b"PK"):
        raise Exception("Le fichier téléchargé n'est pas un ZIP. Vérifie l'URL ou la réponse de l'API.")
    
    zip_file = zipfile.ZipFile(io.BytesIO(resp.content))

