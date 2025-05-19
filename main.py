import matplotlib.pyplot as plt
from Conversion import Conversion
from CollectionDemographique import CollectionDemographique
from reporting import Reporting


def charger_donnees(path="data.csv"):
    with open(path, encoding="utf-8") as f:
        lignes = f.readlines()
    return CollectionDemographique(Conversion.nettoyage(lignes))


def menu():
    data = charger_donnees()
    report = Reporting(data)

    actions = {
        "1": ("Évolution d’un département", report.evolution_population_departement),
        "2": ("Comparaison de départements",   report.comparaison_departements),
        "3": ("Analyse homme / femme",        report.analyse_genre),
        "4": ("Carte population",             report.carte_population_departements),
        "5": ("Âge moyen par département",    report.age_moyen_par_departement),
    }

    while True:
        print("\n=== Menu ===")
        for k, (lbl, _) in actions.items():
            print(f"{k}. {lbl}")
        print("0. Quitter")

        choix = input("Votre choix : ").strip()
        if choix == "0":
            break
        if choix not in actions:
            print("Choix invalide.")
            continue

        # ————————————————————————— paramètres
        if choix in {"1", "3"}:
            dep   = int(input("Département : "))
            debut = int(input("Année début (>=1990) : "))
            fin   = int(input("Année fin   (>=début) : "))
            actions[choix][1](dep, debut, fin)
        elif choix == "2":
            deps  = input("Départements (séparés par des virgules) : ")
            deps  = [int(d.strip()) for d in deps.split(",")]
            debut = int(input("Année début : "))
            fin   = int(input("Année fin   : "))
            actions[choix][1](deps, debut, fin)
        elif choix in {"4", "5"}:
            an = int(input("Année : "))
            actions[choix][1](an)
        plt.show()


if __name__ == "__main__":
    menu()
