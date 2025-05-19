class DonneeDemographique:
    """Enregistrement démographique immuable et ordonnable."""

    __slots__ = ("departement", "annee", "age", "sexe", "population")

    def __init__(self, departement: int, annee: int, age: int,
                 sexe: str, population: int) -> None:
        self.departement = departement
        self.annee = annee
        self.age = age
        self.sexe = sexe
        self.population = population

    # —————————————————————————————————————————— représentation
    def __str__(self) -> str:
        return (f"Département : {self.departement} | Année : {self.annee} | "
                f"Âge : {self.age} | Sexe : {self.sexe} | "
                f"Population : {self.population}")

    # —————————————————————————————————————————— tri naturel
    def __lt__(self, other: "DonneeDemographique") -> bool:  # type: ignore[name-defined]
        if not isinstance(other, DonneeDemographique):
            return NotImplemented
        return (self.departement, self.annee,
                self.age, self.sexe) < (other.departement, other.annee,
                                        other.age, other.sexe)
