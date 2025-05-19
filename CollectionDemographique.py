class CollectionDemographique:
    """Conteneur typé pour les enregistrements démographiques."""

    def __init__(self, liste=None):
        self.liste = list(liste) if liste is not None else []

    # —————————————————————————————————————————— dunder
    def __iter__(self):
        return iter(self.liste)

    def __getitem__(self, index):
        return self.liste[index]

    def __len__(self):
        return len(self.liste)

    def __str__(self):
        return f"{len(self)} enregistrements"

    # —————————————————————————————————————————— utilitaires
    def ajouter(self, enregistrement):
        self.liste.append(enregistrement)

    def sort(self):
        self.liste.sort()          # s’appuie sur __lt__ de DonneeDemographique

    # —————————————————————————————————————————— vues
    def departement(self):
        return [l[0] for l in self.liste]

    def annee(self):
        return [l[3] for l in self.liste]

    def age(self):
        return [l[2] for l in self.liste]

    def sexe(self):
        return [l[1] for l in self.liste]

    def population(self):
        return [l[-1] for l in self.liste]

    # —————————————————————————————————————————— filtres
    def _filtre(self, indice, valeur, egal=True):
        op = (lambda x: x == valeur) if egal else (lambda x: x != valeur)
        return [l for l in self.liste if op(l[indice])]

    def filtre_departement(self, dep):
        return self._filtre(0, dep)

    def filtre_annee(self, an):
        return self._filtre(3, an)

    def filtre_age(self, age):
        return self._filtre(2, age)

    def filtre_sexe(self, sexe):
        return self._filtre(1, sexe)

    def filtre_age_diff(self, age):
        return self._filtre(2, age, egal=False)

    def filtre_sexe_diff(self, sexe):
        return self._filtre(1, sexe, egal=False)
