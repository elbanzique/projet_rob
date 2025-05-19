class Conversion:
    """
    Convertit les lignes CSV brutes en listes normalisées :
    [departement:int, sexe:str, age:int, annee:int, population:int]
    """

    @staticmethod
    def _age_code_to_int(code: str) -> int:
        # Ex. 'Y10T14' → 10, 'Y_GE95' → 95, 'Y_LT5' → 0
        if "_LT" in code:
            return 0
        if "_GE" in code:
            return int(code.split("_GE")[-1])
        digits = "".join(c for c in code if c.isdigit())
        return int(digits[:2]) if digits else 0

    # —————————————————————————————————————————— API publique
    @staticmethod
    def nettoyage(lignes):
        """Renvoie une liste d’enregistrements nettoyés."""
        resultat = []
        for ligne in lignes[1:]:                            # saute l’en-tête
            champs = [c.strip('"') for c in ligne.strip().split(";")]
            if len(champs) < 8:
                continue                                   # ligne incomplète
            try:
                dep = int(champs[0])
                sexe = champs[2]
                age = Conversion._age_code_to_int(champs[3])
                annee = int(champs[6])
                pop = int(champs[7])
                resultat.append([dep, sexe, age, annee, pop])
            except ValueError:
                # au moindre champ non convertible, on ignore la ligne
                continue
        return resultat
