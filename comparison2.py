#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path
from datetime import datetime
import json
import webbrowser
import os

# ================= CONFIG =================
DOSSIER_CSV = './entreprises'
PATTERN = 'Entreprise'
COLONNES_DATES = ['DAT_IMMAT', 'DAT_STAT_IMMAT', 'DAT_DEPO_DECLR', 'DAT_MAJ_INDEX_NOM', 'DAT_CESS_PREVU']
URL_DEBUT = 'https://www.registreentreprises.gouv.qc.ca/REQNA/GR/GR03/GR03A71.RechercheRegistre.MVC/GR03A71?choixdomaine=RegistreEntreprisesQuebec'

# ================= COMPARAISON CSV =================
try:
    print("Démarrage...")

    # --- Charger + nettoyer ---
    def charger(csv_path):
        df = pd.read_csv(csv_path, dtype=str, usecols=lambda c: c in ['NEQ'] + COLONNES_DATES, na_filter=False)
        for col in COLONNES_DATES:
            if col not in df.columns:
                df[col] = ''
        df = df[['NEQ'] + COLONNES_DATES].apply(lambda x: x.str.strip())
        df = df.drop_duplicates('NEQ', keep='first')
        return df

    fichiers = [f for f in Path(DOSSIER_CSV).glob(f'{PATTERN}*.csv')]
    if len(fichiers) < 2:
        raise Exception("Moins de 2 fichiers CSV trouvés.")

    fichiers.sort(key=lambda x: x.stat().st_mtime)
    ancien_f, nouveau_f = fichiers[0], fichiers[-1]
    print(f"Ancien : {ancien_f.name}")
    print(f"Nouveau : {nouveau_f.name}")

    old, new = charger(ancien_f), charger(nouveau_f)

    # --- Nouvelles entreprises ---
    nouvelles = new[~new['NEQ'].isin(old['NEQ'])]['NEQ'].tolist()

    # --- Entreprises modifiées ---
    old_idx = old.set_index('NEQ')
    new_idx = new.set_index('NEQ')
    neq_communs = old_idx.index.intersection(new_idx.index)

    old_commun = old_idx.loc[neq_communs, COLONNES_DATES].copy()
    new_commun = new_idx.loc[neq_communs, COLONNES_DATES].copy()

    diff_mask = old_commun.ne(new_commun)
    modifiees_neq = diff_mask.any(axis=1)
    modifiees = new[new['NEQ'].isin(modifiees_neq[modifiees_neq].index)]['NEQ'].tolist()

    # --- Liste finale ---
    neq_to_scrape = list(set(nouvelles + modifiees))
    print(f"NEQ à scraper : {len(neq_to_scrape)} ({len(nouvelles)} nouvelles, {len(modifiees)} modifiées)")

    if not neq_to_scrape:
        raise Exception("Aucun NEQ à scraper (liste vide).")

    # --- Sauvegarde liste ---
    data = {"liste_neq": neq_to_scrape, "timestamp": datetime.now().isoformat()}
    with open('liste_neq.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

    # --- Redirection simple ---
    js_inject = f"""
    console.log('Redirection vers Registraire...');
    alert('Scraping démarré : {len(neq_to_scrape)} NEQ à traiter');
    setTimeout(() => {{ window.location.href = '{URL_DEBUT}'; }}, 1000);
    """

    html = f"""<!DOCTYPE html><html><head><title>Lancement</title></head><body><script>{js_inject}</script></body></html>"""
    with open('lancer_scraping.html', 'w', encoding='utf-8') as f:
        f.write(html)

    # --- Ouvrir Chrome ---
    html_path = f'file://{os.path.abspath("lancer_scraping.html")}'
    print(f"Ouverture de Chrome : {html_path}")
    webbrowser.open(html_path)

    # --- Rapport ---
    rapport = f"""
RAPPORT AUTOMATISÉ – {datetime.now():%d/%m/%Y %H:%M}

Fichiers comparés :
  Ancien : {ancien_f.name}
  Nouveau : {nouveau_f.name}

Résultats :
  Nouvelles entreprises : {len(nouvelles)}
  Modifiées (dates)     : {len(modifiees)}
  TOTAL À SCRAPER       : {len(neq_to_scrape)}

Action :
  Chrome ouvert (file://lancer_scraping.html)
  Tampermonkey charge liste_neq.json et scrape

Fichiers générés :
  liste_neq.json
  lancer_scraping.html
  *.txt (dans navigateur)
"""
    print(rapport)
    with open(f'rapport_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt', 'w', encoding='utf-8') as f:
        f.write(rapport)

except Exception as e:
    erreur = f"ERREUR : {str(e)}\n\nVérifiez le dossier CSV."
    print(erreur)
    with open(f'erreur_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt', 'w', encoding='utf-8') as f:
        f.write(erreur)
    