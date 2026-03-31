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
COLONNE_VERIF = 'IND_RET_TOUT_POUVR'

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
# 2. Chargement des fichiers
# -------------------------------------------------
print(f"\nChargement des fichiers...")

# Charger avec la colonne NEQ et IND_RET_TOUT_POUVR
old = pd.read_csv(ancien_f, dtype=str, usecols=['NEQ', COLONNE_VERIF], na_filter=False)
new = pd.read_csv(nouveau_f, dtype=str, usecols=['NEQ', COLONNE_VERIF], na_filter=False)

# Supprimer les doublons NEQ
old = old.drop_duplicates(subset='NEQ', keep='first')
new = new.drop_duplicates(subset='NEQ', keep='first')

print(f"   Ancien fichier : {len(old)} entreprises")
print(f"   Nouveau fichier : {len(new)} entreprises")

# -------------------------------------------------
# 3. Identifier les changements
# -------------------------------------------------
print(f"\nAnalyse de la colonne '{COLONNE_VERIF}'...")

# Index par NEQ
old_idx = old.set_index('NEQ')
new_idx = new.set_index('NEQ')

# NEQ communs
neq_communs = old_idx.index.intersection(new_idx.index)
print(f"   NEQ communs : {len(neq_communs)}")

# Détection des changements
modifications = []
for neq in neq_communs:
    old_val = old_idx.at[neq, COLONNE_VERIF]
    new_val = new_idx.at[neq, COLONNE_VERIF]
    
    if old_val != new_val:
        modifications.append({
            'NEQ': neq,
            'ANCIEN_VALEUR': old_val,
            'NOUVEAU_VALEUR': new_val
        })

# Créer DataFrame avec les modifications
mod_df = pd.DataFrame(modifications)

# -------------------------------------------------
# 4. Afficher les résultats
# -------------------------------------------------
print(f"\n{'='*70}")
print(f"RÉSULTATS : Modifications de '{COLONNE_VERIF}'")
print(f"{'='*70}")
print(f"\nNombre de changements détectés : {len(mod_df)}\n")

if len(mod_df) > 0:
    print(mod_df.to_string(index=False))
    print("\n" + "="*70)
    
    # Statistiques
    print("\nSTATISTIQUES :")
    print(f"  • Total d'entreprises modifiées : {len(mod_df)}")
    
    # Détail des changements
    transition = mod_df.groupby(['ANCIEN_VALEUR', 'NOUVEAU_VALEUR']).size()
    print(f"\nDétail des transitions :")
    for (ancien, nouveau), count in transition.items():
        print(f"  • {ancien} → {nouveau} : {count} cas")
else:
    print("Aucune modification détectée dans cette colonne.")

# -------------------------------------------------
# 5. Sauvegarde
# -------------------------------------------------
if len(mod_df) > 0:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'modifications_IND_RET_TOUT_POUVR_{ts}.csv'
    mod_df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n✓ Résultats sauvegardés dans : {output_file}")

print("\n" + "="*70)
print("Analyse terminée !")
print("="*70)
