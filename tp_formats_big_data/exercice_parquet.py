from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
PARQUET_FILE = DATA_DIR / "ventes.parquet"

ventes = pd.DataFrame(
    {
        "vente_id": [1, 2, 3, 4, 5],
        "produit": ["Clavier", "Écran", "Souris", "Écran", "Casque"],
        "categorie": ["Accessoire", "Affichage", "Accessoire", "Affichage", "Audio"],
        "quantite": [2, 1, 3, 2, 1],
        "montant_eur": [79.80, 249.90, 74.70, 499.80, 89.90],
    }
)

# Étape 1 — Écrire le DataFrame au format Parquet.
ventes.to_parquet(PARQUET_FILE, engine="pyarrow", index=False)

# Étape 2 — Examiner les métadonnées et le schéma.
fichier_parquet = pq.ParquetFile(PARQUET_FILE)
print("Schéma Parquet :")
print(fichier_parquet.schema_arrow)

# Étape 3 — Lire et afficher toutes les données.
donnees_lues = pd.read_parquet(PARQUET_FILE, engine="pyarrow")
print("\nToutes les ventes :")
print(donnees_lues.to_string(index=False))

# TODO 1 : relire uniquement les colonnes produit et montant_eur.
colonnes = pd.read_parquet(PARQUET_FILE, engine="pyarrow", columns=["produit", "montant_eur"])
print("\nColonnes sélectionnées :")
print(colonnes.to_string(index=False))

# TODO 2 : filtrer les ventes dont montant_eur >= 100.
ventes_100 = donnees_lues[donnees_lues["montant_eur"] >= 100]
print("\nVentes >= 100 € :")
print(ventes_100.to_string(index=False))

# TODO 3 : calculer le chiffre d'affaires par catégorie avec groupby().
ca = donnees_lues.groupby("categorie")["montant_eur"].sum()
print("\nChiffre d'affaires par catégorie :")
print(ca)