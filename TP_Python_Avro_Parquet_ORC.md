# TP Python — Lire et afficher des fichiers Avro, Parquet et ORC


## Installation

Créer, si possible, un environnement virtuel puis installer les bibliothèques :

```bash
python -m venv .venv
```

Activation sous Linux ou macOS :

```bash
source .venv/bin/activate
```

Activation sous Windows PowerShell :

```powershell
.venv\Scripts\Activate.ps1
```

Installation des dépendances :

```bash
python -m pip install pandas fastavro pyarrow
```

Créer ensuite un dossier de travail :

```text
tp_formats_big_data/
├── exercice_avro.py
├── exercice_parquet.py
├── exercice_orc.py
└── data/
```

> Les fichiers du dossier `data` seront produits automatiquement par les programmes.

---

# Exercice 1 — Lire et afficher un fichier Avro

## Contexte

Apache Avro est un format binaire orienté enregistrements. Le schéma décrivant les données est enregistré avec celles-ci. Avro est notamment adapté aux échanges de messages et à la sérialisation d'événements.

## Travail demandé

1. Créer le fichier `exercice_avro.py`.
2. Définir le schéma Avro d'un relevé de capteur.
3. Enregistrer les quatre relevés fournis dans `data/capteurs.avro`.
4. Relire le fichier et afficher son schéma.
5. Afficher chaque enregistrement sur une ligne.
6. Afficher uniquement les relevés dont la température dépasse 22 °C.
7. Calculer la température moyenne.

## Code de départ

```python
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

# TODO 2 : calculer et afficher la température moyenne avec mean().
```

## Résultat attendu — extrait

```text
Enregistrements :
{'capteur_id': 'C001', 'zone': 'Laboratoire', 'temperature': 21.8, ...}
...
Température moyenne : 22.25 °C
```

## Questions

1. Où le schéma est-il stocké dans le cas d'Avro ?
2. Pourquoi le fichier doit-il être ouvert avec les modes `wb` et `rb` ?
3. Quel avantage Avro présente-t-il pour l'échange d'événements entre applications ?

---

# Exercice 2 — Lire et afficher un fichier Parquet

## Contexte

Apache Parquet est un format de stockage binaire orienté colonnes. Il permet de ne lire que les colonnes utiles et convient particulièrement à l'analyse de grandes quantités de données.

## Travail demandé

1. Créer le fichier `exercice_parquet.py`.
2. Construire un DataFrame représentant des ventes.
3. L'enregistrer dans `data/ventes.parquet` sans conserver l'index Pandas.
4. Afficher le schéma du fichier et toutes ses données.
5. Lire uniquement les colonnes `produit` et `montant_eur`.
6. Afficher uniquement les ventes de montant supérieur ou égal à 100 €.
7. Calculer le chiffre d'affaires par catégorie.

## Code de départ

```python
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
# Indice : utiliser le paramètre columns de pd.read_parquet().

# TODO 2 : filtrer les ventes dont montant_eur >= 100.

# TODO 3 : calculer le chiffre d'affaires par catégorie avec groupby().
```

## Résultat attendu — extrait

```text
Colonnes sélectionnées :
 produit  montant_eur
 Clavier        79.80
   Écran       249.90
...

Chiffre d'affaires par catégorie :
categorie
Accessoire    154.5
Affichage     749.7
Audio          89.9
```

## Questions

1. Que signifie « format orienté colonnes » ?
2. Quel est l'intérêt du paramètre `columns` lors de la lecture ?
3. Dans quels types de traitements Parquet est-il préférable à Avro ?

---

# Exercice 3 — Lire et afficher un fichier ORC

## Contexte

Apache ORC (*Optimized Row Columnar*) est également un format orienté colonnes. Il offre compression, index internes et statistiques, et est très utilisé dans les environnements Hadoop et Hive.

## Travail demandé

1. Créer le fichier `exercice_orc.py`.
2. Construire une table Arrow représentant des observations d'espèces.
3. L'enregistrer dans `data/observations.orc`.
4. Afficher le schéma et toutes les données.
5. Lire uniquement les colonnes `espece` et `confiance`.
6. Afficher les observations dont la confiance est supérieure ou égale à 0,90.
7. Compter le nombre d'observations par site.

## Code de départ

```python
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
# Indice : fichier_orc.read(columns=[...]).

# TODO 2 : filtrer les lignes dont confiance >= 0.90.

# TODO 3 : compter les observations par site avec value_counts().
```

## Résultat attendu — extrait

```text
Observations avec une confiance >= 0.90 :
 observation_id site               espece  confiance  validee
            101  CDG   Faucon crécerelle       0.96     True
            103  ZAG Mésange charbonnière      0.93     True
            105  ZAG            Hirondelle      0.91     True
```

## Questions

1. Quelles ressemblances existe-t-il entre ORC et Parquet ?
2. Pourquoi convertit-on ici la table Arrow en DataFrame Pandas ?
3. Dans quel écosystème ORC est-il historiquement très utilisé ?

---

# Exercice 4 — Comparaison des formats

Compléter le tableau suivant après avoir réalisé les trois exercices.

| Critère | Avro | Parquet | ORC |
|---|---|---|---|
| Organisation principale | À compléter | À compléter | À compléter |
| Schéma inclus | À compléter | À compléter | À compléter |
| Lecture de colonnes ciblées | À compléter | À compléter | À compléter |
| Usage principal | À compléter | À compléter | À compléter |
| Bibliothèque Python utilisée | À compléter | À compléter | À compléter |

Comparer également la taille des trois fichiers :

```python
from pathlib import Path

for chemin in Path("data").iterdir():
    if chemin.is_file():
        print(f"{chemin.name:25} : {chemin.stat().st_size:6} octets")
```

> Attention : avec un jeu de données aussi petit, les métadonnées occupent une part importante du fichier. La comparaison des tailles ne permet donc pas de conclure sur les performances de compression à grande échelle.

## Questions de synthèse

1. Quel format choisiriez-vous pour transporter des événements entre microservices ? Justifier.
2. Quel format choisiriez-vous pour analyser seulement quelques colonnes d'une table comportant des millions de lignes ? Justifier.
3. Parquet et ORC sont-ils des formats lisibles directement comme un fichier texte ?
4. Pourquoi est-il important de connaître le schéma avant d'exploiter un fichier de données ?

---

# Extensions facultatives

Pour aller plus loin :

1. ajouter dix enregistrements à chaque jeu de données ;
2. introduire une valeur manquante et observer le comportement du schéma ;
3. écrire le fichier Parquet avec une compression `snappy`, puis `gzip` ;
4. mesurer le temps de lecture avec `time.perf_counter()` ;
5. créer un programme `conversion.py` qui lit le fichier Avro et produit un fichier Parquet ;
6. tester les fichiers avec DuckDB ou Apache Spark.

## Livrables attendus

L'étudiant remet une archive contenant :

```text
nom_prenom_tp_formats.zip
├── exercice_avro.py
├── exercice_parquet.py
├── exercice_orc.py
├── comparaison.md
└── captures/
```

Le fichier `comparaison.md` doit contenir le tableau complété, les réponses aux questions de synthèse et une courte conclusion de cinq à dix lignes.

## Critères d'évaluation proposés

| Élément évalué | Points |
|---|---:|
| Exercice Avro fonctionnel | 4 |
| Exercice Parquet fonctionnel | 4 |
| Exercice ORC fonctionnel | 4 |
| Filtres, statistiques et affichage | 3 |
| Tableau comparatif et réponses | 3 |
| Qualité du code et commentaires | 2 |
| **Total** | **20** |

## Rapport


À la fin de ce TP, Rédiger un rapport :

- expliquer le rôle des formats Avro, Parquet et ORC ;
- créer un petit jeu de données en Python ;
- enregistrer des données dans chacun de ces formats ;
- lire et afficher le contenu d'un fichier ;
- consulter son schéma et sélectionner certaines données ;
- comparer les caractéristiques des trois formats.