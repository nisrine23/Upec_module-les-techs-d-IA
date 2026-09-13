from pathlib import Path
from statistics import mean

from fastavro import parse_schema, reader, writer


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
AVRO_FILE = DATA_DIR / "capteurs.avro"

schema = {
    "type": "record",
    "name": "ReleveCapteur",
    "namespace": "fr.upec.iot",
    "fields": [
        {"name": "capteur_id", "type": "string"},
        {"name": "zone", "type": "string"},
        {"name": "temperature", "type": "double"},
        {"name": "humidite", "type": "int"},
        {"name": "actif", "type": "boolean"},
    ],
}

releves = [
    {"capteur_id": "C001", "zone": "Laboratoire", "temperature": 21.8, "humidite": 45, "actif": True},
    {"capteur_id": "C002", "zone": "Couloir", "temperature": 23.4, "humidite": 41, "actif": True},
    {"capteur_id": "C003", "zone": "Salle serveur", "temperature": 19.7, "humidite": 38, "actif": True},
    {"capteur_id": "C004", "zone": "Atelier", "temperature": 24.1, "humidite": 52, "actif": False},
]

# Étape 1 — Écrire les données au format Avro.
with AVRO_FILE.open("wb") as fichier:
    writer(fichier, parse_schema(schema), releves)

# Étape 2 — Lire le fichier, récupérer le schéma et les enregistrements.
with AVRO_FILE.open("rb") as fichier:
    lecteur = reader(fichier)
    schema_lu = lecteur.writer_schema
    donnees_lues = list(lecteur)

print("Schéma Avro :")
print(schema_lu)

print("\nEnregistrements :")
for releve in donnees_lues:
    print(releve)

# TODO 1 : afficher les relevés dont la température est supérieure à 22 °C.
print("\nRelevés avec température > 22 °C :")
for releve in donnees_lues:
    if releve["temperature"] > 22:
        print(releve)

# TODO 2 : calculer et afficher la température moyenne avec mean().
temperatures = [releve["temperature"] for releve in donnees_lues]
print(f"\nTempérature moyenne : {mean(temperatures)} °C")