from pathlib import Path

import pyarrow as pa
import pyarrow.orc as orc


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
ORC_FILE = DATA_DIR / "observations.orc"

table = pa.table(
    {
        "observation_id": [101, 102, 103, 104, 105],
        "site": ["CDG", "CDG", "ZAG", "CLUJ", "ZAG"],
        "espece": ["Faucon crécerelle", "Renard roux", "Mésange charbonnière", "Lièvre", "Hirondelle"],
        "confiance": [0.96, 0.84, 0.93, 0.78, 0.91],
        "validee": [True, False, True, False, True],
    }
)

# Étape 1 — Écrire la table au format ORC.
orc.write_table(table, ORC_FILE)

# Étape 2 — Ouvrir le fichier et afficher son schéma.
fichier_orc = orc.ORCFile(ORC_FILE)
print("Schéma ORC :")
print(fichier_orc.schema)

# Étape 3 — Lire toute la table, puis la convertir en DataFrame.
table_lue = fichier_orc.read()
donnees_lues = table_lue.to_pandas()

print("\nToutes les observations :")
print(donnees_lues.to_string(index=False))

# TODO 1 : relire seulement les colonnes espece et confiance.
table_partielle = fichier_orc.read(columns=["espece", "confiance"])
print("\nColonnes sélectionnées :")
print(table_partielle.to_pandas().to_string(index=False))

# TODO 2 : filtrer les lignes dont confiance >= 0.90.
filtre = donnees_lues[donnees_lues["confiance"] >= 0.90]
print("\nObservations avec une confiance >= 0.90 :")
print(filtre.to_string(index=False))

# TODO 3 : compter les observations par site avec value_counts().
print("\nObservations par site :")
print(donnees_lues["site"].value_counts())