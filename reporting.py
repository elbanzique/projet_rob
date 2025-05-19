import matplotlib.pyplot as plt
from CollectionDemographique import CollectionDemographique


class Reporting:
    """Module d’affichage des analyses démographiques."""

    def __init__(self, data: CollectionDemographique):
        self.data = data            # déjà une CollectionDemographique

    # —————————————————————————————————————————— helpers
    def _total_pop(self, dep, an):
        return sum(l[-1] for l in self.data.liste
                   if l[0] == dep and l[3] == an)

    def _pop_by(self, dep, an, sexe):
        return sum(l[-1] for l in self.data.liste
                   if l[0] == dep and l[3] == an and l[1] == sexe)

    # —————————————————————————————————————————— graphiques
    def evolution_population_departement(self, dep, debut=1990, fin=2024):
        annees = list(range(debut, fin + 1))
        pops = [self._total_pop(dep, a) for a in annees]

        plt.figure(figsize=(7, 4))
        plt.plot(annees, pops, marker="o")
        plt.title(f"Population du département {dep} ({debut}-{fin})")
        plt.xlabel("Année")
        plt.ylabel("Population")
        plt.grid(True, linestyle="--", alpha=.3)
        return plt

    def comparaison_departements(self, deps, debut=1990, fin=2024):
        annees = list(range(debut, fin + 1))
        plt.figure(figsize=(7, 4))
        for dep in deps:
            pops = [self._total_pop(dep, a) for a in annees]
            plt.plot(annees, pops, marker="o", label=f"Dép. {dep}")
        plt.title("Comparaison des populations")
        plt.xlabel("Année")
        plt.ylabel("Population")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=.3)
        return plt

    def analyse_genre(self, dep, debut=1990, fin=2024):
        annees = list(range(debut, fin + 1))
        hommes = [self._pop_by(dep, a, "M") for a in annees]
        femmes = [self._pop_by(dep, a, "F") for a in annees]

        plt.figure(figsize=(7, 4))
        plt.plot(annees, hommes, marker="o", label="Hommes")
        plt.plot(annees, femmes, marker="o", label="Femmes")
        plt.title(f"Répartition H/F – département {dep}")
        plt.xlabel("Année")
        plt.ylabel("Population")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=.3)
        return plt

    # ➀ Carte population et ➁ âge moyen → versions simplifiées en barplot
    def carte_population_departements(self, an=2024):
        deps = sorted(set(l[0] for l in self.data))
        pops = [self._total_pop(dep, an) for dep in deps]

        plt.figure(figsize=(8, 4))
        plt.bar(deps, pops)
        plt.title(f"Population par département en {an}")
        plt.xlabel("Département")
        plt.ylabel("Population")
        return plt

    def age_moyen_par_departement(self, an=2024):
        deps = sorted(set(l[0] for l in self.data))
        moyennes = []
        for dep in deps:
            lignes = [l for l in self.data if l[0] == dep and l[3] == an]
            pop_tot = sum(l[-1] for l in lignes)
            age_moy = (sum(l[2] * l[-1] for l in lignes) / pop_tot) if pop_tot else 0
            moyennes.append(age_moy)

        plt.figure(figsize=(8, 4))
        plt.bar(deps, moyennes)
        plt.title(f"Âge moyen par département en {an}")
        plt.xlabel("Département")
        plt.ylabel("Âge moyen")
        return plt
