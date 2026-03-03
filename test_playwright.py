from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Lancer le navigateur Chromium en mode non headless
    browser = p.firefox.launch(headless=False)
    context = browser.new_context(
            extra_http_headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "en-US,en;q=0.8",
                "connection": "keep-alive",
                "content-type": "application/json; charset=UTF-8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            }
        )
    page = context.new_page()
    page.set_default_timeout(50000)

    # Naviguer vers la page
        # Ajout des cookies (exemple, à adapter si besoin)

        # Naviguer vers la page
    page.goto("https://www.registreentreprises.gouv.qc.ca/reqna/gr/gr03/gr03a71.rechercheregistre.mvc/gr03a71?choixdomaine=RegistreEntreprisesQuebecz")

    # Remplir le champ de recherche
    page.fill('input#Objet', "humano")

    # Cocher la case des conditions d'utilisation
    page.check('#ConditionUtilisationCochee')

    # Soumettre le formulaire
    page.click('button[type="submit"]')

    # Attendre que les résultats soient chargés (ajuster le sélecteur selon les éléments dynamiques)
    page.wait_for_selector('div#content')  # Attendre jusqu'à 15 secondes pour un tableau de résultats

    # Récupérer le contenu HTML généré
    html_content = page.content()

    # Afficher ou sauvegarder le contenu
    print(html_content)
    with open("resultats.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    # Attendre une entrée utilisateur avant de fermer
    input("Appuie sur Entrée pour fermer le navigateur...")

    # Fermer le navigateur
    browser.close()