"""
BasisSet.py contains the BasisSet class, which contains data pertaining to the functions of multiple atoms under
multiple basis sets in a Gaussian format.
"""

# Westmont Computational Chemistry ToolKit © 2022 by Riley Johnson, Curtis Barnhart is licensed under CC BY-NC-SA 4.0
# https://github.com/rijohnson2023/MOD
# http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1

from BasisAtom import BasisAtom


class BasisSet:
    """
    The BasisSet class is basically a simple wrapper for an ordered list of BasisAtom objects. It can be indexed like
    a dictionary to return a dictionary of atomic symbols to atom functions for just the atoms under a specific basis
    set (e.g. basisSetObject["6-31+g*"]).

    Getting the string representation of a BasisSet object returns a string of all the atoms' functions in it in order
    of increasing atomic number and separated by "****".
    """

    def __init__(self, data: list[BasisAtom]):
        self.data = sorted(data)

    def __repr__(self):
        """
        :return: a string of all the atoms' functions in self.data in order of increasing atomic number and with each
        atom's functions followed by "\n****"
        """

        return "\n****\n".join((str(atom) for atom in self.data)) + "\n****"

    def __getitem__(self, item: str) -> dict[str, str]:
        """
        Allows indexing ot a BasisSet object (e.g. basisSetObject["6-31+g*"]).

        :param item: name of a basis set
        :return: a dictionary of atomic symbols to atom functions for just the atoms under the specified basis set
        """
        atoms = {}
        for atom in self.data:
            if atom.basis == item:
                atoms[atom.name] = atom.funcs
        return atoms
