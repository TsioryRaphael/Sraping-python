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
COLONNES_INTERET = [
    'NEQ', 'DAT_IMMAT', 'IND_RET_TOUT_POUVR', 
    'COD_STAT_IMMAT', 'DAT_STAT_IMMAT', 'DAT_MAJ_INDEX_NOM'
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
# 2. Chargement + nettoyage
# -------------------------------------------------
def charger_et_nettoyer(csv_path):
    """Charge le CSV et sélectionne les colonnes d'intérêt"""
    try:
        df = pd.read_csv(csv_path, dtype=str, na_filter=False)
        # Vérifier quelles colonnes existent
        cols_dispo = [c for c in COLONNES_INTERET if c in df.columns]
        df = df[cols_dispo]
        # Supprimer doublons NEQ
        df = df.drop_duplicates(subset='NEQ', keep='first')
        return df
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")
        raise

old = charger_et_nettoyer(ancien_f)
new = charger_et_nettoyer(nouveau_f)

print(f"\nAncien fichier : {len(old)} entreprises")
print(f"Nouveau fichier : {len(new)} entreprises")

# -------------------------------------------------
# 3. Filtrer entreprises immatriculées
# -------------------------------------------------
# Une entreprise immatriculée doit avoir un DAT_IMMAT
old_immat = old[old['DAT_IMMAT'].notna() & (old['DAT_IMMAT'] != '')].copy()
new_immat = new[new['DAT_IMMAT'].notna() & (new['DAT_IMMAT'] != '')].copy()

print(f"Anciennes immatriculées : {len(old_immat)}")
print(f"Nouvelles immatriculées : {len(new_immat)}")

# -------------------------------------------------
# 4. Détecter changements sur IND_RET_TOUT_POUVR
# -------------------------------------------------
# NEQ communs
neq_communs = list(set(old_immat['NEQ']).intersection(set(new_immat['NEQ'])))
print(f"NEQ immatriculés communs : {len(neq_communs)}")

# Index par NEQ pour accès rapide
old_idx = old_immat.set_index('NEQ')
new_idx = new_immat.set_index('NEQ')

# Détecter les changements sur IND_RET_TOUT_POUVR
changements = []
for neq in neq_communs:
    try:
        old_val = old_idx.at[neq, 'IND_RET_TOUT_POUVR'] if 'IND_RET_TOUT_POUVR' in old_idx.columns else ''
        new_val = new_idx.at[neq, 'IND_RET_TOUT_POUVR'] if 'IND_RET_TOUT_POUVR' in new_idx.columns else ''
        
        # Si les valeurs sont différentes
        if old_val != new_val:
            changements.append({
                'NEQ': neq,
                'DAT_IMMAT': old_idx.at[neq, 'DAT_IMMAT'] if 'DAT_IMMAT' in old_idx.columns else '',
                'IND_RET_TOUT_POUVR_ANCIEN': old_val,
                'IND_RET_TOUT_POUVR_NOUVEAU': new_val,
                'COD_STAT_IMMAT_ANCIEN': old_idx.at[neq, 'COD_STAT_IMMAT'] if 'COD_STAT_IMMAT' in old_idx.columns else '',
                'COD_STAT_IMMAT_NOUVEAU': new_idx.at[neq, 'COD_STAT_IMMAT'] if 'COD_STAT_IMMAT' in new_idx.columns else '',
                'DAT_MAJ_INDEX_NOM_ANCIEN': old_idx.at[neq, 'DAT_MAJ_INDEX_NOM'] if 'DAT_MAJ_INDEX_NOM' in old_idx.columns else '',
                'DAT_MAJ_INDEX_NOM_NOUVEAU': new_idx.at[neq, 'DAT_MAJ_INDEX_NOM'] if 'DAT_MAJ_INDEX_NOM' in new_idx.columns else '',
            })
    except Exception as e:
        print(f"Erreur pour NEQ {neq}: {e}")

changements_df = pd.DataFrame(changements)
print(f"\n✓ Changements détectés sur IND_RET_TOUT_POUVR : {len(changements)}")

# -------------------------------------------------
# 5. Nouvelles immatriculations
# -------------------------------------------------
neq_nouveau = set(new_immat['NEQ']) - set(old_immat['NEQ'])
print(f"✓ Nouvelles immatriculations : {len(neq_nouveau)}")

if neq_nouveau:
    nouvelles_immat = new_immat[new_immat['NEQ'].isin(neq_nouveau)].copy()
    # Ajouter colonnes pour indiquer que c'est nouveau
    nouvelles_immat['IND_RET_TOUT_POUVR_ANCIEN'] = 'N/A (nouveau)'
    nouvelles_immat['IND_RET_TOUT_POUVR_NOUVEAU'] = nouvelles_immat['IND_RET_TOUT_POUVR']
else:
    nouvelles_immat = pd.DataFrame()

# -------------------------------------------------
# 6. Sauvegarde + rapport
# -------------------------------------------------
ts = datetime.now().strftime("%Y%m%d_%H%M%S")

# Sauvegarder les changements
if not changements_df.empty:
    cols = ['NEQ', 'DAT_IMMAT', 'IND_RET_TOUT_POUVR_ANCIEN', 'IND_RET_TOUT_POUVR_NOUVEAU', 
            'COD_STAT_IMMAT_ANCIEN', 'COD_STAT_IMMAT_NOUVEAU', 
            'DAT_MAJ_INDEX_NOM_ANCIEN', 'DAT_MAJ_INDEX_NOM_NOUVEAU']
    changements_df = changements_df[cols]
    changements_df.to_csv(f'modifications_IND_RET_TOUT_POUVR_{ts}.csv', index=False, encoding='utf-8')

# Sauvegarder les nouvelles immatriculations
if not nouvelles_immat.empty:
    nouvelles_immat.to_csv(f'nouvelles_immatriculees_IND_RET_TOUT_POUVR_{ts}.csv', index=False, encoding='utf-8')

# Rapport synthétique
rapport = f"""\
RAPPORT ANALYSE ENTREPRISES IMMATRICULÉES – {datetime.now():%d/%m/%Y %H:%M}

Fichiers comparés
  Ancien : {ancien_f.name}
  Nouveau : {nouveau_f.name}

ENTREPRISES IMMATRICULÉES
  Anciennes immatriculées       : {len(old_immat)}
  Nouvelles immatriculées       : {len(new_immat)}
  Communes                      : {len(neq_communs)}

COLONNE IND_RET_TOUT_POUVR (Retrait pouvoirs conseil d'administration)
  Changements détectés         : {len(changements)}
  Nouvelles immatriculations   : {len(neq_nouveau)}

Résumé des changements IND_RET_TOUT_POUVR :
  (0 → 1) Pouvoirs retirés      : {len(changements_df[(changements_df['IND_RET_TOUT_POUVR_ANCIEN'] == '0') & (changements_df['IND_RET_TOUT_POUVR_NOUVEAU'] == '1')]) if len(changements_df) > 0 else 0}
  (1 → 0) Pouvoirs restaurés    : {len(changements_df[(changements_df['IND_RET_TOUT_POUVR_ANCIEN'] == '1') & (changements_df['IND_RET_TOUT_POUVR_NOUVEAU'] == '0')]) if len(changements_df) > 0 else 0}
  (vide → 0 ou 1)              : {len(changements_df[(changements_df['IND_RET_TOUT_POUVR_ANCIEN'].isin(['', 'NaN'])) & (changements_df['IND_RET_TOUT_POUVR_NOUVEAU'].notna())]) if len(changements_df) > 0 else 0}

Fichiers générés
  modifications_IND_RET_TOUT_POUVR_{ts}.csv (changements détectés)
  nouvelles_immatriculees_IND_RET_TOUT_POUVR_{ts}.csv (nouvelles immatriculations)
  rapport_immatriculees_{ts}.txt (ce rapport)
"""

with open(f'rapport_immatriculees_{ts}.txt', 'w', encoding='utf-8') as f:
    f.write(rapport)

print("\n" + "="*70)
print(rapport)
print("="*70)
print("Analyse terminée !")
