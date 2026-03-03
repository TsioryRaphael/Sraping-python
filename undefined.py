import csv
import json

def load_neq_from_csv(path):
    """Charge proprement la colonne 'neq' depuis un CSV (avec ou sans header)."""
    neq_set = set()
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        # Cherche la colonne contenant 'neq'
        try:
            neq_index = next(i for i, h in enumerate(header) if "neq" in h.lower())
        except StopIteration:
            # pas d'en-tête : on repart de la première ligne
            f.seek(0)
            neq_index = 0
            reader = csv.reader(f)
        for row in reader:
            if len(row) > neq_index:
                val = row[neq_index].strip()
                if val:
                    neq_set.add(val)
    return neq_set


# Charger les deux fichiers CSV
neq_initial = load_neq_from_csv("neq initial.csv")
neq_final = load_neq_from_csv("neq final.csv")

# Comparer
neq_manquants = sorted(neq_initial - neq_final)

print(f"✅ NEQ manquants : {len(neq_manquants)}")

# Sauvegarde
with open("neq_a_relancer.json", "w", encoding="utf-8") as f:
    json.dump(neq_manquants, f, indent=2, ensure_ascii=False)

print("💾 Fichier 'neq_a_relancer.txt' créé avec succès.")
