"""
BasisAtom.py contains the BasisAtom class, which contains the function data of one atom under one basis set.
"""

# Westmont Computational Chemistry ToolKit © 2022 by Riley Johnson, Curtis Barnhart is licensed under CC BY-NC-SA 4.0
# https://github.com/rijohnson2023/MOD
# http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1

from dataclasses import dataclass


@dataclass(frozen=True, repr=False, order=True)
class BasisAtom:
    """
    The BasisAtom class contains the function data of one atom under one basis set. The atom is identified by its atomic
    number "number", and the basis its functions are under the name of its basis "basis". "funcs" contains the data of
    the atoms functions under the specified basis set. BasisAtom is an immutable class and has comparison methods so
    that basisAtom1 < basisAtom2 returns True if basisAtom1 has a lower atomic number than basisAtom2 etc.
    """
    number: int
    basis: str
    funcs: str

    def __repr__(self):
        return self.funcs
