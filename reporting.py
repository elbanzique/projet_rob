import matplotlib.pyplot as plt
from CollectionDemographique import CollectionDemographique


class Reporting:
    """
    Génère les analyses démographiques.
    """

    def __init__(self, data: CollectionDemographique):
        self.data = data

    # ---------------------------------------------------------------- helpers
    def _total_pop(self, dep, an):
        """Population totale du département pour l'année `an` (T si dispo, sinon M+F)."""
        tot = sum(l[-1] for l in self.data
                  if l[0] == dep and l[3] == an and l[1] == "T")
        if tot:
            return tot
        return sum(l[-1] for l in self.data
                   if l[0] == dep and l[3] == an and l[1] in {"M", "F"})

    def _pop_by(self, dep, an, sexe):
        """Population d’un sexe donné (M ou F) pour le département et l’année."""
        return sum(l[-1] for l in self.data
                   if l[0] == dep and l[3] == an and l[1] == sexe)

    def _pop_by_age_total(self, dep, an, age_min, age_max=None):
        """
        Population (M+F) comprise entre age_min et age_max pour une année donnée.
        """
        if age_max is None:
            age_max = age_min
        return sum(
            l[-1] for l in self.data
            if (l[0] == dep and l[3] == an and l[1] in {"M", "F"}
                and age_min <= l[2] <= age_max)
        )

    # ---------------------------------------------------------- analyses de base
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
        for d in deps:
            pops = [self._total_pop(d, a) for a in annees]
            plt.plot(annees, pops, marker="o", label=f"Dép. {d}")
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

    def carte_population_departements(self, an=2024):
        deps = sorted({l[0] for l in self.data})
        pops = [self._total_pop(dep, an) for dep in deps]

        plt.figure(figsize=(8, 4))
        plt.bar(deps, pops)
        plt.title(f"Population par département en {an}")
        plt.xlabel("Département")
        plt.ylabel("Population")
        return plt

    def age_moyen_par_departement(self, an=2024):
        deps = sorted({l[0] for l in self.data})
        moyennes = []
        for dep in deps:
            # on prend T si disponible, sinon M+F pour le total
            pop_tot = self._total_pop(dep, an)
            # moy = Σ(age * pop) / pop_tot
            ligne_dep = [l for l in self.data
                         if l[0] == dep and l[3] == an and l[1] in {"M", "F"}]
            if not pop_tot:
                moyennes.append(0)
            else:
                moyennes.append(sum(l[2] * l[-1] for l in ligne_dep) / pop_tot)

        plt.figure(figsize=(8, 4))
        plt.bar(deps, moyennes)
        plt.title(f"Âge moyen par département en {an}")
        plt.xlabel("Département")
        plt.ylabel("Âge moyen")
        return plt

    # ---------------------------------------------- natalité / mortalité réels
    def taux_natalite_mortalite(self, dep=62, debut=1991, fin=2024):
        """
        Natalité  : (pop 0–4 ans / 5) / pop_totale(M+F) * 1000  [‰]
        Mortalité : pop ≥85 ans / pop_totale(M+F) * 1000       [‰]
        """
        annees = list(range(debut, fin + 1))
        natalite, mortalite = [], []

        for an in annees:
            # population totale = M + F
            pop_tot = sum(l[-1] for l in self.data
                          if l[0] == dep and l[3] == an and l[1] in {"M", "F"})
            if pop_tot == 0:
                natalite.append(0)
                mortalite.append(0)
                continue

            # on récupère la tranche 0–4 ans puis on divise par 5 pour ne garder qu’une cohorte
            naissances = self._pop_by_age_total(dep, an, 0, 4) / 5
            deces      = self._pop_by_age_total(dep, an, 85, 130)  # ≥85 ans

            natalite.append(naissances / pop_tot * 1000)
            mortalite.append(deces / pop_tot * 1000)

        plt.figure(figsize=(7, 4))
        plt.plot(annees, natalite,  marker="o", label="Natalité (‰)")
        plt.plot(annees, mortalite, marker="o", label="Mortalité (‰)")
        plt.title(f"Taux natalité / mortalité – dép. {dep}")
        plt.xlabel("Année")
        plt.ylabel("Taux pour 1 000 hab.")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=.3)

        return plt, natalite, mortalite

    # --------------------------------------------- projection lissée 5 ans
    def projection_population(self, dep=62, base_year=2024, fin=2050):
        """
        Projection à partir des taux nat. / mort. moyens (5 dernières années).
        """
        debut_calc = max(base_year - 4, 1991)
        _, nat_list, mort_list = self.taux_natalite_mortalite(
            dep, debut_calc, base_year
        )
        taux_nat = sum(nat_list) / len(nat_list) if nat_list else 0
        taux_mort = sum(mort_list) / len(mort_list) if mort_list else 0

        pop = self._total_pop(dep, base_year)
        annees, pops = [base_year], [pop]

        for an in range(base_year + 1, fin + 1):
            births = taux_nat / 1000 * pop
            deaths = taux_mort / 1000 * pop
            pop = pop + births - deaths
            annees.append(an)
            pops.append(pop)

        plt.figure(figsize=(7, 4))
        plt.plot(annees, pops, marker="o")
        plt.title(
            f"Projection démographique dép. {dep} ({base_year}→{fin}) "
            f"(nat. {taux_nat:.1f}‰ / mort. {taux_mort:.1f}‰ – moy. 5 ans)"
        )
        plt.xlabel("Année")
        plt.ylabel("Population projetée")
        plt.grid(True, linestyle="--", alpha=.3)
        return plt
