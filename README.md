# Projet CP1 : Analyse Démographique

Ce projet consiste à analyser et visualiser des données démographiques à partir d'un fichier CSV. Le programme permet de filtrer les données, de les organiser, et de les représenter graphiquement.

## Fichiers principaux

* `main.py` : point d'entrée du programme, propose un menu interactif.
* `Conversion.py` : nettoyage et transformation des données CSV.
* `donnedemographique.py` : définit la classe DonneeDemographique.
* `CollectionDemographique.py` : gère une liste de données avec tri et filtres.
* `reporting.py` : génère les graphiques avec matplotlib.
* `data.csv` : fichier de données démographiques.

## Fonctionnalités

* Évolution de la population d'un département.
* Comparaison entre plusieurs départements.
* Analyse par sexe.
* Carte de la population par département.
* Calcul de l'âge moyen par département.

## Lancement

Dans le terminal :

```bash
python main.py
```

Assurez-vous que `data.csv` se trouve dans le même répertoire que `main.py`.
