from playwright.sync_api import sync_playwright
import zipfile
import pandas as pd
import sys

def download_with_playwright(nom_entreprise):
    url = "https://www.registreentreprises.gouv.qc.ca/RQAnonymeGR/GR/GR03/GR03A2_22A_PIU_RecupDonnPub_PC/FichierDonneesOuvertes.aspx"

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        print("⏳ Téléchargement en cours...")
        page.goto("about:blank")
        with page.expect_download() as download_info:
            page.evaluate(f"window.location.href = '{url}'")
        download = download_info.value
        download.save_as("entreprises.zip")
        print("✅ Fichier sauvegardé sous entreprises.zip")
        browser.close()

# ---------Lecture du ZIP et extraction du CSV-------------------
        # # Lire le ZIP
        # with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        #     csv_name = [n for n in zip_ref.namelist() if n.endswith('.csv')][0]
        #     with zip_ref.open(csv_name) as f:
        #         df = pd.read_csv(f, sep=";", dtype=str, low_memory=False)

        # browser.close()
# -------Filtrer et sauvegarder le CSV-------------------
    # # Filtrer
    # result = df[df['RaisonSociale'].str.contains(nom_entreprise, case=False, na=False)]

    # # Sauvegarder le résultat
    # out_file = f"result_{nom_entreprise}.csv"
    # result.to_csv(out_file, index=False, sep=";")
    # print(f"✅ Résultat sauvegardé dans {out_file}")

if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("❌ Donne un nom d'entreprise en argument")
    #     sys.exit(1)

    nom = input("Entrez le nom de l'entreprise : ")

    download_with_playwright(nom)
