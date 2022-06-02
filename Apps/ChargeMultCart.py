"""

"""

# Westmont Computational Chemistry ToolKit © 2022 by Riley Johnson, Curtis Barnhart is licensed under CC BY-NC-SA 4.0
# https://github.com/rijohnson2023/MOD
# http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1


class ChargeMultCart:

    def __init__(self, charge: int, mult: int, atoms: tuple[tuple[str, tuple[float, float, float]]]):
        self.charge = charge
        self.mult = mult
        self.atoms = atoms

    def __repr__(self):
        chargeMult = "{: d} {:d}\n".format(self.charge, self.mult)

        atomIterator = (
            " {:<2s}{:>27.8f}{:>14.8f}{:>14.8f}".format(atomData[0].capitalize(), *atomData[1])
            for atomData in self.atoms)

        return chargeMult + "\n".join(atomIterator)

    def getCharge(self) -> int:
        return self.charge

    def getMult(self) -> int:
        return self.mult

    def getCarts(self) -> tuple[tuple[str, tuple[float, float, float]]]:
        return self.atoms

    def getAtoms(self) -> list[str]:
        return [atomData[0] for atomData in self.atoms]
