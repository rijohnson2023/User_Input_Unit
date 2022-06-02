"""
ui_menus.py contains the tools to collect user input from the command line and format it into a header or footer object
"""
import math
import os
import random
import Apps.PeriodicTable as PeriodicTable


# Westmont Computational Chemistry ToolKit © 2022 by Riley Johnson, Curtis Barnhart is licensed under CC BY-NC-SA 4.0
# https://github.com/rijohnson2023/MOD
# http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1


def clearConsole():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("clr")


def Menu1(dataPop: dict[str: int], dataRecent: list[str], inputTitle: str) -> list[str]:
    """
    This menu returns a list of strings. 
    It takes in the integer related to the option,
    and then it add the option to a list.

    This cycle completes until the user specifies option 1,
    which is no further input.

    The final option is other, where the user may specify a
    string that was not offered as an option.

    This string is then added to the data, if provided.
    """
    COLUMN_WIDTH = 30

    sortedPopular = sorted(dataPop.keys(), key=lambda key: dataPop[key], reverse=True)

    choice = None
    UI_M1_list = []

    while choice != 1:
        clearConsole()
        UI_Choices = ["No additional inputs."] + sortedPopular[:5] + dataRecent[:4] + ["--Other", "--Remove Input"]
        display(UI_Choices, COLUMN_WIDTH)

        print("CURRENT HEADER:")
        for headerElement in UI_M1_list:
            print(headerElement)
        print("-" * (COLUMN_WIDTH * 2 + 9))

        print("Select your option:")

        choice = intInput(len(UI_Choices))
        if choice is None:
            continue

        if UI_Choices[choice - 1] == "--Other":
            UI_M1_list.append(input("\nEnter the custom input:\n"))
        elif UI_Choices[choice - 1] == "--Remove Input":
            removeChoice = None
            UI_M1_list.append("I didn't mean it! (Exits without removing anything)")

            while removeChoice is None:
                clearConsole()
                display(UI_M1_list, COLUMN_WIDTH)

                removeChoice = intInput(len(UI_M1_list))

            if removeChoice != len(UI_M1_list):
                UI_M1_list.pop(len(UI_M1_list) - 1)
            UI_M1_list.pop(removeChoice - 1)
        else:  # Choosing item
            UI_M1_list.append(UI_Choices[choice - 1])
            if UI_Choices[choice - 1] in sortedPopular:
                sortedPopular.remove(UI_Choices[choice - 1])
            if UI_Choices[choice - 1] in dataRecent:
                dataRecent.remove(UI_Choices[choice - 1])

    return UI_M1_list


def atomsInput(basisSetChoice: str, alreadySelected: set[str] = None, cleanConsole: bool = True) -> tuple[
               set[str], list[str]]:
    if alreadySelected is None:
        alreadySelected = set()

    atomsReal = False
    troubleAtoms = []
    while not atomsReal:
        currentSelection = set()
        if cleanConsole:
            clearConsole()
        for troubleAtom in troubleAtoms:
            print(troubleAtom)

        atomChoices = input("Enter all the atoms for Basis Set %s, delimited by spaces.\n"
                            "Identify atoms by atomic number or symbol (case insensitive).\n" % basisSetChoice)
        atomChoices = atomChoices.split()

        atomsReal = True
        troubleAtoms = []
        for atom in atomChoices:
            if atom.lower() in PeriodicTable.SYMBOLS:  # If they have input the symbol directly
                atom = atom.lower().capitalize()
                if atom in alreadySelected:
                    troubleAtoms.append(
                        "\033[91mProblem occurred: %s has already been selected under a basis set.\033[00m " % atom)
                    atomsReal = False
                elif atom in currentSelection:
                    troubleAtoms.append(
                        "\033[91mProblem occurred: %s has already been selected under this basis set.\033[00m " % atom)
                    atomsReal = False
                else:
                    currentSelection.add(atom)
            elif atom in (str(atomicNum) for atomicNum in PeriodicTable.NUMBERS):  # If they entered the atomic number
                atomSym = PeriodicTable.getSymbol(int(atom))
                if atomSym in alreadySelected:
                    troubleAtoms.append(
                        "\033[91mProblem occurred: %s has already been selected under a basis set.\033[00m " % atomSym.capitalize())
                    atomsReal = False
                elif atomSym in currentSelection:
                    troubleAtoms.append(
                        "\033[91mProblem occurred: %s has already been selected under this basis set.\033[00m " % atomSym.capitalize())
                    atomsReal = False
                else:
                    atomChoices[atomChoices.index(atom)] = atomSym
                    currentSelection.add(atomSym)
            else:
                troubleAtoms.append("\033[91mProblem occurred: %s cannot be identified as an atom.\033[00m " % atom)
                atomsReal = False

    alreadySelected = alreadySelected.union(currentSelection)

    return alreadySelected, atomChoices


def basisSetInput(alreadySelectedBS: set[str] = None, cleanConsole: bool = True) -> tuple[set[str], str]:
    if alreadySelectedBS is None:
        alreadySelectedBS = set()

    basisSetChoice = ""
    problem = ""
    while basisSetChoice not in PeriodicTable.BSE_VERSIONS.keys() or problem:
        if cleanConsole:
            clearConsole()
        if problem:
            print(problem)
        problem = ""

        basisSetChoice = input("Enter a Basis Set:\n").lower()
        if basisSetChoice in alreadySelectedBS:
            problem = "\033[91mProblem occurred: %s has already been selected as a Basis Set.\033[00m " % basisSetChoice
        elif basisSetChoice not in PeriodicTable.BSE_VERSIONS.keys():
            problem = "\033[91mProblem occurred: %s cannot be identified as a Basis Set.\033[00m " % basisSetChoice

    alreadySelectedBS.add(basisSetChoice)
    return alreadySelectedBS, basisSetChoice


def editBasisSet(basisSetData: list[str], alreadySelected: set[str], cleanConsole: bool = True) -> tuple[set[str], list[str]]:
    WIDTH = 20
    basisSetName = basisSetData[0]
    atoms = basisSetData[1:]
    choices = [atom.capitalize() for atom in atoms] + ["--Remove All", "--Add Atoms", "--Editing Complete"]

    choice = None
    while choice != len(choices):
        choices = [atom.capitalize() for atom in atoms] + ["--Remove All", "--Add Atoms", "--Editing Complete"]
        if cleanConsole:
            clearConsole()
        print(basisSetName)
        display(choices, width=WIDTH)
        print("Select an atom to remove that atom.")
        print("-" * (WIDTH * 2 + 9))

        choice = intInput(len(choices))
        if choice == len(choices) - 1:  # If they want to add atoms
            alreadySelected, addedAtoms = atomsInput(basisSetName, alreadySelected)
            atoms = atoms + addedAtoms
        elif choice == len(choices) - 2:  # If they want to remove the basis set
            removed = set(atoms)
            alreadySelected = alreadySelected.difference(removed)
            return alreadySelected, []
        elif choice is not len(choices):
            alreadySelected.remove(atoms.pop(int(choice) - 1))

    return alreadySelected, [basisSetName] + atoms


def menu2ByBasisSet():
    WIDTH = 30
    basisSets = []
    alreadySelectedAtoms = set()
    alreadySelectedBS = set()
    viewBySymbol = True

    while True:
        if viewBySymbol:
            basisSetsDisplay = [bsData[0] + ": " + ", ".join((atomSymbol.capitalize() for atomSymbol in bsData[1:])) for
                                bsData in basisSets]
            displayOptions = basisSetsDisplay + ["--Add Basis Set", "--View by Atomic Number",
                                                 "--Basis Set Selection Complete"]
        else:
            basisSetsDisplay = [bsData[0] + ": " + ", ".join((str(PeriodicTable.getNumber(atomSymbol)) for atomSymbol in bsData[1:])) for
                                bsData in basisSets]
            displayOptions = basisSetsDisplay + ["--Add Basis Set", "--View by Atomic Symbol",
                                                 "--Basis Set Selection Complete"]
        clearConsole()

        display(displayOptions, width=WIDTH)
        print("Select a Basis Set to add or remove atoms under it.")
        print("-" * (WIDTH * 2 + 9))

        choice = intInput(len(displayOptions))
        if choice is None:
            continue

        if displayOptions[choice - 1] == "--Basis Set Selection Complete":
            break
        elif displayOptions[choice - 1] == "--View by Atomic Number":
            # If they are viewing by opposite atom format
            viewBySymbol = False
        elif displayOptions[choice - 1] == "--View by Atomic Symbol":
            # If they are viewing by opposite atom format
            viewBySymbol = True
        elif displayOptions[choice - 1] == "--Add Basis Set":
            # If they are adding a new Basis Set
            clearConsole()

            # Selecting a Basis Set
            alreadySelectedBS, basisSetChoice = basisSetInput(alreadySelectedBS)

            # Selecting atoms under that Basis Set
            # TODO: Make sure that you can't enter a Basis Set twice
            alreadySelectedAtoms, atomChoices = atomsInput(basisSetChoice, alreadySelectedAtoms)

            if atomChoices:
                basisSets.append([basisSetChoice] + atomChoices)

        else:
            # If they are editing a Basis Set
            alreadySelectedAtoms, editedBasisSet = editBasisSet(basisSets[choice - 1], alreadySelectedAtoms)
            if not editedBasisSet:
                basisSets.pop(choice - 1)
            else:
                basisSets[choice - 1] = editedBasisSet

    basisSetFormatted = dict()
    for basisSet in basisSets:
        basisSetAtoms = set()
        for atom in basisSet[1:]:
            basisSetAtoms.add(atom)
        basisSetFormatted[basisSet[0]] = basisSetAtoms

    return basisSetFormatted


def menu2ByAtom():
    pass


def intInput(end: int, start: int = 1, inputMethod=input):
    try:
        answer = inputMethod()
        if start <= int(answer) <= end:
            return int(answer)
        else:
            return
    except ValueError:
        return


def display(items: list[str], width: int = 20) -> None:
    HALF_LENGTH = (len(items) + 1) // 2
    UNEVEN = len(items) != HALF_LENGTH * 2
    MAX_INDEX_LENGTH = math.ceil(math.log10(len(items) + 1))

    if UNEVEN:
        items = list(items)
        items.append("")

    print("-" * ((width + 3 + MAX_INDEX_LENGTH) * 2 + 1))

    for i in range((len(items) + 1) // 2):
        height = (max((len(items[i])), len(items[HALF_LENGTH + i])) + width - 1) // width
        # TODO: add in documentation that an empty string will do wacky things to it
        stringSegments = []
        lineNum = 0
        while lineNum < height:
            for item in (items[i], items[HALF_LENGTH + i]):
                # Setting prefix
                if lineNum == 0:
                    if item is items[i]:
                        index = i + 1
                    else:
                        index = HALF_LENGTH + i + 1
                    prefix = "[{:{:d}d}] ".format(index, MAX_INDEX_LENGTH)
                    if UNEVEN and item is items[-1]:
                        prefix = " " * (3 + MAX_INDEX_LENGTH)
                else:
                    prefix = " " * (3 + MAX_INDEX_LENGTH)

                charsLeft = len(item) - lineNum * width
                if charsLeft > width:
                    # If there's plenty left cut off what you need and add it
                    stringSegments.append(prefix + item[lineNum * width: (lineNum + 1) * width])
                elif charsLeft <= 0:
                    # If there's no more left then just add whitespace
                    stringSegments.append(prefix + " " * width)
                else:
                    # If there's just a little bit left then add it
                    stringSegments.append(prefix + item[lineNum * width:] + " " * (width - charsLeft))
            lineNum += 1

        for j in range(0, len(stringSegments), 2):
            print(stringSegments[j], stringSegments[j + 1])

    print("-" * ((width + 3 + MAX_INDEX_LENGTH) * 2 + 1))


def test_Menu1():
    Link0MostPop = {'nprocshared=60': 5, 'mem=60gb': 4, 'chk=__filename__.chk': 3, 'cpu=4': 1, 'ssh=command': 2,
                    'lindaworkers=(lina1,linda2,linda3)': 1}
    Link0MostRecent = ['nprocshared', 'oldraw=(__filename__,i8lab)', 'oldmatrix', 'lindaworkers',
                       'nproclinda', 'oldraw', 'oldmatrix=(__filename__,i8lab)',
                       'oldraw=(__filename__,i4lab)', 'chk', 'ssh=command', 'cpu', 'oldchk',
                       'oldmatrix=(__filename__,i4lab)', 'mem', 'gpucpu']
    inputName = "link0 inputs"
    UI_List = Menu1(dataPop=Link0MostPop, dataRecent=Link0MostRecent, inputTitle=inputName)
    print(UI_List)


# Data from scrape
allKeywords = ['admp', 'bd', 'bomd', 'cachesize', 'casscf', 'cbs', 'cbsextrapolate', 'ccd', 'charge', 'chkbasis', 'cid',
               'cis', 'cndo', 'complex', 'constants', 'counterpoise', 'cphf', 'density', 'densityfit', 'dft', 'dftb',
               'eet', 'eomccsd', 'ept', 'external', 'extrabasis', 'field', 'fmm', 'force', 'freq', 'gen', 'genchk',
               'geom', 'gfinput', 'gfprint', 'gn', 'guess', 'gvb', 'hf', 'huckel', 'indo', 'integral', 'iop', 'irc',
               'ircmax', 'link0', 'lsda', 'maxdisk', 'mindo3', 'mndo', 'mm', 'mp', 'name', 'nmr', 'oniom',
               'optimization', 'output', 'pbc', 'polar', 'population', 'pressure', 'prop', 'pseudo', 'punch', 'qci',
               'restart', 'sac-ci', 'scale', 'scan', 'scf', 'scrf', 'semi-empirical', 'sp', 'sparse', 'stable',
               'symmetry', 'td', 'temperature', 'test', 'testmo', 'trackio', 'transformation', 'units', 'volume', 'w1',
               'window', 'zindo']
Link0UserOpt = {'%nprocshared=60\n%mem=60gb\n': 5, '%nprocshared=4\n%mem=16gb\n': 5, 'custom': 5}
Link0Keywords = ['%nprocshared', '%oldraw=(__filename__,i8lab)', '%rwf', '%oldmatrix', '%lindaworkers', '%nproclinda',
                 '#\xa0section', '%oldraw', '%oldmatrix=(__filename__,i8lab)', '%oldraw=(__filename__,i4lab)', '%chk',
                 '%ssh=command', '%cpu', '%oldchk', '%oldmatrix=(__filename__,i4lab)', '%mem', '%gpucpu']

# Example of the string selection menu
test_Menu1()

# Example of the Basis Set selection menu
b = menu2ByBasisSet()
