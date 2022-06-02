"""

"""

# Westmont Computational Chemistry ToolKit © 2022 by Riley Johnson, Curtis Barnhart is licensed under CC BY-NC-SA 4.0
# https://github.com/rijohnson2023/MOD
# http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1

import os
from ChargeMultCart import ChargeMultCart
from PeriodicTable import getSymbol


def readFile(filename: str):
    """
    readFile takes a filename and

    :param filename:
    :return: A ChargeMultCart object that contains the data
    """
    if os.path.exists(filename):
        if filename.endswith(".gjf"):
            with open(filename) as file:
                return readGJF(file)
        elif filename.endswith(".log"):
            with open(filename) as file:
                return readLOG(file)
        else:
            print("File was not .gjf or .log file.")
    else:
        print("File not found.")


def readGJF(file):
    """

    """
    data = file.read().split("\n\n")[2].split("\n")

    charge, mult = map(int, data[0].split())

    atoms = []
    for line in data[1:]:
        atom, c1, c2, c3 = line.split()
        carts = tuple(map(float, (c1, c2, c3)))
        atoms.append((atom, carts))

    return ChargeMultCart(charge, mult, tuple(atoms))


def readLOG(file):
    """
    readLOG
    """
    text = file.read()

    # Finding the charge and multiplicity data
    chargeMultLine = text.find(" Charge = ")
    endOfLine = text.find("\n", chargeMultLine)
    chargeMult = text[chargeMultLine: endOfLine].split()
    charge = int(chargeMult[2])
    mult = int(chargeMult[5])

    # Finding the atom data
    SECTION_DELIMITER = " ---------------------------------------------------------------------\n"
    keyLinePosition = text.find("                           !   Optimized Parameters   !")
    headerBegin = text.find(SECTION_DELIMITER, keyLinePosition) + len(SECTION_DELIMITER)
    headerEnd = text.find(SECTION_DELIMITER, headerBegin) + len(SECTION_DELIMITER)
    dataEnd = text.find(SECTION_DELIMITER, headerEnd) - 1
    data = text[headerEnd: dataEnd].split("\n")

    atoms = []
    for line in data:
        centerNum, atomNum, atomType, c1, c2, c3 = line.split()
        carts = tuple(map(float, (c1, c2, c3)))
        atoms.append((getSymbol(int(atomNum)), carts))

    return ChargeMultCart(charge, mult, tuple(atoms))
