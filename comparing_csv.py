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

# Détail des changements (dates + autres champs)
# ---
# Pour analyser si un changement de date peut s'accompagner d'autres modifications,
# on compare toutes les colonnes communes à l'ancien et au nouveau fichier.
# Cela permet de détecter les changements sur les champs additionnels (statut, nom, etc.)
# tout en conservant la détection sur les dates.

# On relit les deux fichiers en entier (tous les champs) pour comparer au niveau des colonnes.
full_old = pd.read_csv(ancien_f, dtype=str, na_filter=False)
full_new = pd.read_csv(nouveau_f, dtype=str, na_filter=False)

# Assurer que la colonne NEQ existe et qu'il n'y a pas de doublons NEQ.
for df, name in [(full_old, ancien_f.name), (full_new, nouveau_f.name)]:
    if 'NEQ' not in df.columns:
        raise SystemExit(f"Le fichier {name} ne contient pas de colonne NEQ.")

full_old = full_old.drop_duplicates(subset='NEQ', keep='first')
full_new = full_new.drop_duplicates(subset='NEQ', keep='first')

# Index par NEQ pour accès rapide
full_old_idx = full_old.set_index('NEQ')
full_new_idx = full_new.set_index('NEQ')

# Colonnes communes (hors NEQ) à comparer
common_cols = [c for c in full_old.columns if c in full_new.columns and c != 'NEQ']

# Détail des changements
# On se limite aux NEQ identifiés comme ayant un changement de date.
details = []
for neq in modifiees_neq[modifiees_neq].index:
    row = {'NEQ': neq}
    for col in common_cols:
        old_val = full_old_idx.at[neq, col]
        new_val = full_new_idx.at[neq, col]
        if old_val != new_val:
            row[col] = new_val
    if len(row) > 1:
        details.append(row)

modifiees_detail = pd.DataFrame(details)
if not modifiees_detail.empty:
    cols = ['NEQ'] + [c for c in modifiees_detail.columns if c != 'NEQ']
    modifiees_detail = modifiees_detail[cols]

print(f"Modifiées (dates + autres champs) : {len(modifiees['NEQ'].unique())}")

# -------------------------------------------------
# 5. Sauvegarde + rapport
# -------------------------------------------------
ts = datetime.now().strftime("%Y%m%d_%H%M%S")

# Pour les nouvelles entreprises, on veut toutes les colonnes disponibles dans le fichier
# original (table Entreprise). On utilise le CSV déjà chargé (`full_new`).
# assurer que la colonne NEQ existe même si le CSV n'en contient pas (improbable)
if 'NEQ' not in full_new.columns:
    raise SystemExit(f"Le fichier {nouveau_f.name} ne contient pas de colonne NEQ.")

nouvelles_completes = full_new[full_new['NEQ'].isin(nouvelles['NEQ'])].copy()

nouvelles_completes.to_csv(f'nouvelles_entreprises_{ts}.csv', index=False, encoding='utf-8')
modifiees_detail.to_csv(f'modifiees_{ts}.csv', index=False, encoding='utf-8')

# Générer fichier JS avec seulement les entreprises modifiées
all_neq = sorted(list(set(modifiees['NEQ'])))

# Format: 10 numéros par ligne, entre guillemets
lines = []
for i in range(0, len(all_neq), 10):
    batch = all_neq[i:i+10]
    line = ', '.join([f'"{neq}"' for neq in batch])
    if i + 10 < len(all_neq):
        line += ","
    lines.append(line)

js_content = "let numbers = [\n" + "\n".join(lines) + "\n];"
with open(f'neq_list_{ts}.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

rapport = f"""\
RAPPORT DE COMPARAISON – {datetime.now():%d/%m/%Y %H:%M}

Fichiers comparés
  Ancien : {ancien_f.name}
  Nouveau : {nouveau_f.name}

Résultats
  Nouvelles entreprises          : {len(nouvelles)}
  Entreprises avec changements    : {len(modifiees['NEQ'].unique())}
  Total NEQ à traiter            : {len(all_neq)}

Fichiers générés
  nouvelles_entreprises_{ts}.csv
  modifiees_{ts}.csv
  neq_list_{ts}.js
"""

with open(f'rapport_comparaison_{ts}.txt', 'w', encoding='utf-8') as f:
    f.write(rapport)

print("\n" + "="*60)
print(rapport)
print("="*60)
print("Comparaison terminée !")