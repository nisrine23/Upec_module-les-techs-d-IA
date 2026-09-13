# Comparaison Avro / Parquet / ORC

| Critère | Avro | Parquet | ORC |
|---|---|---|---|
| Organisation principale | Orienté lignes (enregistrements) | Orienté colonnes | Orienté colonnes |
| Schéma inclus | Oui (JSON dans l'en-tête) | Oui (métadonnées) | Oui (métadonnées) |
| Lecture de colonnes ciblées | Non | Oui | Oui |
| Usage principal | Échange de messages / streaming / écriture | Analytique / OLAP / gros volumes | Analytique / Hadoop / Hive |
| Bibliothèque Python | fastavro | pyarrow / pandas | pyarrow.orc |

## Réponses aux questions

### Exercice 1 — Avro
1. Le schéma est stocké **dans le fichier Avro lui-même**, dans l'en-tête (métadonnée `avro.schema` au format JSON).
2. Le fichier doit être ouvert en `wb`/`rb` car Avro est un format **binaire** : un mode texte corromprait les données.
3. Avro est adapté à l'échange d'événements : schéma embarqué, format compact, évolution de schéma supportée, très utilisé en streaming (Kafka).

### Exercice 2 — Parquet
1. « Orienté colonnes » = les données sont stockées **colonne par colonne** au lieu de ligne par ligne. Cela permet de ne lire que les colonnes utiles.
2. Le paramètre `columns` évite de charger en mémoire les colonnes inutiles → gain de temps et de mémoire sur gros volumes.
3. Parquet est préférable à Avro pour les **traitements analytiques** (agrégations, OLAP, Spark, DuckDB) sur de grandes tables.

### Exercice 3 — ORC
1. ORC et Parquet partagent : format binaire, orienté colonnes, compression, schéma et statistiques internes.
2. On convertit en DataFrame Pandas pour bénéficier de méthodes pratiques (filtres, `groupby`, `value_counts`, affichage).
3. ORC est historiquement très utilisé dans l'écosystème **Hadoop / Hive**.

## Questions de synthèse
1. **Transport d'événements entre microservices** → Avro : schéma embarqué, compact, adapté au streaming.
2. **Analyser quelques colonnes sur des millions de lignes** → Parquet (ou ORC) : lecture colonnaire, I/O minimaux.
3. **Lisibles comme un fichier texte ?** → Non, Avro, Parquet et ORC sont **binaires** ; il faut une bibliothèque dédiée.
4. **Pourquoi connaître le schéma ?** → Pour interpréter les octets, typer les colonnes, valider les données et gérer l'évolution du format.

## Conclusion
Ce TP a permis de manipuler trois formats de stockage binaires majeurs. Avro s'est révélé simple pour écrire et relire des enregistrements avec un schéma embarqué, ce qui le destine au streaming. Parquet et ORC, orientés colonnes, facilitent la sélection partielle de colonnes et conviennent à l'analyse de gros volumes. Les bibliothèques Python `fastavro`, `pandas` et `pyarrow` offrent une API concise pour lire, écrire et convertir ces formats. La comparaison des tailles sur un si petit jeu n'est pas significative : c'est à grande échelle que ces formats révèlent leurs avantages.