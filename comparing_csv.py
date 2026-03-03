#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path
from datetime import datetime

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
DOSSIER_CSV = './entreprises'
PATTERN     = 'Entreprise'
COLONNES_DATES = [
    'DAT_IMMAT', 'DAT_STAT_IMMAT', 'DAT_DEPO_DECLR',
    'DAT_MAJ_INDEX_NOM', 'DAT_CESS_PREVU'
]

# -------------------------------------------------
# 1. Trouver les deux fichiers
# -------------------------------------------------
print("Recherche des fichiers...")
fichiers = [f for f in Path(DOSSIER_CSV).glob(f'{PATTERN}*.csv') if f.is_file()]
if len(fichiers) < 2:
    raise SystemExit("Moins de 2 fichiers trouvés.")

fichiers.sort(key=lambda p: p.stat().st_mtime)
ancien_f, nouveau_f = fichiers[0], fichiers[-1]
print(f"Ancien : {ancien_f.name}")
print(f"Nouveau : {nouveau_f.name}")

# -------------------------------------------------
# 2. Chargement + nettoyage + suppression doublons
# -------------------------------------------------
def charger_et_dedupliquer(csv_path):
    df = pd.read_csv(csv_path,
                     dtype=str,
                     usecols=lambda c: c in ['NEQ'] + COLONNES_DATES,
                     na_filter=False)
    # Remplir colonnes manquantes
    for col in COLONNES_DATES:
        if col not in df.columns:
            df[col] = ''
    df = df[['NEQ'] + COLONNES_DATES].apply(lambda x: x.str.strip())
    
    # Supprimer doublons NEQ → garder la première occurrence
    avant = len(df)
    df = df.drop_duplicates(subset='NEQ', keep='first')
    apres = len(df)
    if avant != apres:
        print(f"   → {avant - apres} doublons NEQ supprimés dans {csv_path.name}")
    return df

old = charger_et_dedupliquer(ancien_f)
new = charger_et_dedupliquer(nouveau_f)

# -------------------------------------------------
# 3. Nouvelles entreprises
# -------------------------------------------------
nouvelles = new[~new['NEQ'].isin(old['NEQ'])].copy()
print(f"Nouvelles : {len(nouvelles)}")

# -------------------------------------------------
# 4. Entreprises modifiées (dates)
# -------------------------------------------------
old_idx = old.set_index('NEQ')
new_idx = new.set_index('NEQ')

# NEQ communs
neq_communs = old_idx.index.intersection(new_idx.index)

# Comparaison
diff_mask = pd.DataFrame(False, index=neq_communs, columns=COLONNES_DATES)
for col in COLONNES_DATES:
    diff_mask[col] = old_idx.loc[neq_communs, col] != new_idx.loc[neq_communs, col]

modifiees_neq = diff_mask.any(axis=1)
modifiees = new[new['NEQ'].isin(modifiees_neq[modifiees_neq].index)].copy()

# Détail des changements
details = []
for neq in modifiees_neq[modifiees_neq].index:
    for col in COLONNES_DATES:
        if diff_mask.at[neq, col]:
            details.append({
                'NEQ': neq,
                'COLONNE_MODIFIEE': col,
                'ANCIENNE_VALEUR': old_idx.at[neq, col],
                'NOUVELLE_VALEUR': new_idx.at[neq, col]
            })
modifiees_detail = pd.DataFrame(details)

print(f"Modifiées (dates) : {len(modifiees['NEQ'].unique())}")

# -------------------------------------------------
# 5. Sauvegarde + rapport
# -------------------------------------------------
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
nouvelles.to_csv(f'nouvelles_entreprises_{ts}.csv', index=False, encoding='utf-8')
modifiees_detail.to_csv(f'modifiees_dates_{ts}.csv', index=False, encoding='utf-8')

rapport = f"""\
RAPPORT DE COMPARAISON – {datetime.now():%d/%m/%Y %H:%M}

Fichiers comparés
  Ancien : {ancien_f.name}
  Nouveau : {nouveau_f.name}

Résultats
  Nouvelles entreprises          : {len(nouvelles)}
  Entreprises avec dates changées: {len(modifiees['NEQ'].unique())}

Fichiers générés
  nouvelles_entreprises_{ts}.csv
  modifiees_dates_{ts}.csv
"""

with open(f'rapport_comparaison_{ts}.txt', 'w', encoding='utf-8') as f:
    f.write(rapport)

print("\n" + "="*60)
print(rapport)
print("="*60)
print("Comparaison terminée !")