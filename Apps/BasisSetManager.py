"""
BasisSetManager.py contains the tools to retrieve the functions of multiple atoms under multiple basis sets either from
local files in a ./BasisCache directory or, failing that, from basissetexchange.org.
"""

# Westmont Computational Chemistry ToolKit © 2022 by Riley Johnson, Curtis Barnhart is licensed under CC BY-NC-SA 4.0
# https://github.com/rijohnson2023/MOD
# http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1

import requests
import os
from PeriodicTable import getName, getSymbol, BSE_VERSIONS
from BasisSet import BasisSet
from BasisAtom import BasisAtom
from Exceptions import BasisSetException


class BasisSetManager:
    """

    """
    cache = {}

    def __init__(self, basisCacheLocation="../BasisCache", inputMethod=input):
        self.bsCacheDir = basisCacheLocation
        self.inputMethod = inputMethod

    def getBasisSet(self, data: dict[str, set[int]]) -> BasisSet:
        """
        getBasisSet returns a BasisSet object that contains the functions of the atoms and basis sets specified in "data".

        It does this by first searching the class variable "cache", then by looking for relevant files in the directory
        ./BasisCache, and then making a request for the data from basissetexchange.org. It tries these one at a time, since
        each method is faster than the ones listed after it, only moving on to the next method if the data cannot be found
        via the last method.

        If the data for a particular atom "a" cannot be found under a particular basis set "b", getBasisSet will search
        through files in the ./BasisCache directory looking for alternate basis sets that do have information for the atom
        "a". If no such data can be found for at least one element, the program exits without returning a BasisSet object.

        :param data: dict[str, set[int]] whose keys are the names of basis sets and whose values are sets of integers
        describing which atoms (by atomic number) the user wants to know the functions of under the basis set key. Basis set
        names must be lower case. e.g. {"6-31+g*": {1, 7, 8}, "6-311+g": {3, 4, 5, 19}}
        :return: BasisSet object describing the requested basis set and atoms
        """
        basisSetAtoms = []  # basisSetAtoms is a list of BasisAtom objects that will be put into the BasisSet object
        # that is returned

        # Sets up directory for storing basis set/atom function info files
        if not os.path.isdir(self.bsCacheDir):
            os.mkdir(self.bsCacheDir)

        for basis in data.keys():
            for element in data[basis]:  # Iterates over each desired element in each desired basis

                # First check cache dictionary to see if the information was stored during program runtime
                funcs = BasisSetManager.checkCache(basis, element)

                if funcs is None:
                    # Second check BasisCache directory to see if the information is already locally stored on computer
                    funcs = self.checkMemory(basis, element)

                    if funcs is None:
                        # Third attempt to retrieve it from basissetexchange.org
                        funcs = BasisSetManager.checkWeb(basis, element)

                        # If the information cannot be found on basissetexchange.org, checks local files for alternate
                        # basis sets (any files that end with "[atomic symbol].bs")
                        if funcs is None:
                            working = set()
                            for filename in os.listdir(self.bsCacheDir):
                                if filename.endswith(getSymbol(element) + ".bs"):
                                    working.add(filename.split(";")[0])
                            if working:
                                print("The element " + getName(
                                    element) + " cannot be found in the basis set " + basis + ".")
                                print("Alternative local basis sets containing data for the element " + getName(
                                    element) + " include:")
                                for example in working:
                                    print("\t" + example)

                                # gets decision from user to use an alternate basis set
                                newBasis = self.inputMethod("To retry with one of these basis sets, enter its name (q to quit): ")
                                while newBasis not in working:
                                    if newBasis == "q":
                                        raise BasisSetException("The element " + getName(element) + " cannot be found in the basis set " + basis + ".")
                                    newBasis = self.inputMethod(
                                        "To retry with one of these basis sets, enter its name (q to quit): ")
                                funcs = self.checkMemory(newBasis, element)
                            else:  # if alternate basis sets cannot be found for any atom, program quits
                                raise BasisSetException("The element " + getName(element) + " cannot be found in the basis set " + basis + ".")
                        else:
                            # Updates secondary and primary storage of basis set/atom info if it could be found online
                            self.addMemory(basis, element, funcs)
                    else:
                        # Updates primary storage of basis set/atom info if it could be found in secondary storage
                        BasisSetManager.addCache(basis, element, funcs)

                basisSetAtoms.append(BasisAtom(element, basis, funcs))

        return BasisSet(basisSetAtoms)

    @staticmethod
    def checkCache(basis: str, element: int) -> str:
        """
        checkCache searches for a key "[basis];[element]" in the global dictionary "cache" and returns its contents (the
        functions of the element "element" under the basis "basis") if it exists.

        :param basis: name of basis
        :param element: atomic number of element
        :return: functions of atom "element" under basis "basis", if they exist
        """
        if basis + ";" + getSymbol(element) in BasisSetManager.cache:
            return BasisSetManager.cache[basis + ";" + getSymbol(element)]

    @staticmethod
    def addCache(basis: str, element: int, funcs: str) -> None:
        """
        addCache takes the functions "funcs" of the atom "element" under the basis "basis" and adds them to the global d
        ictionary "cache" so that the key is "[basis];[element]" and the value is the str "funcs".

        :param basis: name of basis
        :param element: atomic number of element
        :param funcs: functions of atom "element" under basis "basis"
        :return: None
        """
        BasisSetManager.cache[basis + ";" + getSymbol(element)] = funcs

    def checkMemory(self, basis: str, element: int) -> str:
        """
        checkMemory searches for a file called "./BasisCache/[basis];[element].bs" and returns its contents (the functions of
        the element "element" under the basis "basis") if it exists.

        :param basis: name of basis
        :param element: atomic number of element
        :return: functions of atom "element" under basis "basis", if they exist
        """
        if basis + ";" + getSymbol(element) + ".bs" in os.listdir(self.bsCacheDir):
            with open(self.bsCacheDir + "/" + basis + ";" + getSymbol(element) + ".bs", "r") as file:
                funcs = file.read()
            return funcs

    def addMemory(self, basis: str, element: int, funcs: str) -> None:
        """
        addMemory takes the functions "funcs" of the atom "element" under the basis "basis" and writes them to a file
        "./BasisCache/[basis];[element].bs"

        :param basis: name of basis
        :param element: atomic number of element
        :param funcs: functions of atom "element" under basis "basis"
        :return: None
        """
        BasisSetManager.addCache(basis, element, funcs)
        with open(self.bsCacheDir + "/" + basis + ";" + getSymbol(element) + ".bs", "w") as file:
            file.write(funcs)

    @staticmethod
    def checkWeb(basis: str, element: int) -> str:
        """
        checkWeb looks up the functions of the atom "element" under the basis "basis" on www.basissetexchange.org and
        returns them if they exist under that basis set.

        :param basis: name of basis
        :param element: atomic number of element
        :return: functions of atom "element" under basis "basis", if they exist
        """
        url = "https://www.basissetexchange.org/download_basis/basis/" + basis + "/format/gaussian94/?version=" + \
            str(BSE_VERSIONS[basis]) + "&" + "elements=" + str(element)

        raw = requests.get(url)
        if raw.status_code == 200:  # If the request was successful, extracts the atom's functions and returns them
            text = raw.text.split("!----------------------------------------------------------------------")[-1]
            text = text.split("****")[0][3:-1]
            return text
