"""
ui.Menus.py contains the tools to collect user input from the command line and format it into a header or footer object 
"""

import random
import pyinputplus as pyip
import pprint as pp

# Westmont Computational Chemistry ToolKit © 2022 by Riley Johnson, Curtis Barnhart is licensed under CC BY-NC-SA 4.0
# https://github.com/rijohnson2023/MOD
# http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1


def find_kth_largest(nums: list[int], k: int) -> int:
    """
    Quick Select: Returns the value kth largest value in an unsorted array
    """
    # choosing a random number in the origional array to begin sorting the data into 3 arrays
    pivot = random.choice(nums)
    # Left right and mid are all arrays
    left = [x for x in nums if x > pivot]
    mid = [x for x in nums if x == pivot]
    right = [x for x in nums if x < pivot]

    # Counting the number of elements in the left and mid array
    L,M = len(left), len(mid)

    if k <= L:   # if k, the kth largest int, is less than the length of the left array, then K is in the left array 
        return find_kth_largest(left,k)
    elif k > (L+M): # if k, the kth largest int is greater than the length of the left and middle array, then k must be in the right array
        return find_kth_largest(right, k-(L+M))
    else: # if K is not in the left or right array, then it in the middle array, and the middle array only contains the pivot number
        return mid[0]


def kth_largest_items(data: dict[str:int], k: int=4) -> dict :
    """
    Returns a new dictionary that keeps the items whose values are greater than the value of the kth largest element.
    """
    # Identify the fourth highest value in the dict
    value = find_kth_largest(list(data.values()),k)

    # Create a new dict by filter the arg dict for the top k elements based on their value
    newDict = dict(filter(lambda elem: elem[1] >= value,data.items()))

    return newDict


def constr_opt(freqUsed: dict, recUsed: list, NoAddOption = False, Other=True, optCount=4) -> list[str]:
    # Construct list for menu
    ui_Choices = list()

    # Insert the additional input option
    if NoAddOption == True : ui_Choices.insert(0,"[1] No Additional Inputs")

    # Adding all of the most recently used keywords to the options 
    [ui_Choices.append("[%d] %s" % (index1, elem)) for index1, elem in enumerate(recUsed,2)if recUsed.index(elem) < optCount]

    # Adding the most frequently used data to the options
    [ui_Choices.append("[%d] %s"% (index2, elem)) for index2, elem in enumerate(freqUsed.keys(),len(ui_Choices)+ 1)]

    # Adding the option to type in a keyword not shown
    if Other == True : ui_Choices.append('[%d] Other:' % (len(ui_Choices) + 1))

    return ui_Choices


def valididate_other(input:str):
    pass


def Menu(freqUsed: dict[str:int], recUsed: list[str], inputTitle: str, AddInputs: bool=True, optCount: int=4) -> list[str]:
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
    # Filter the data dictionary to ony include the top "k" keys:value pairs
    mostUsed = kth_largest_items(freqUsed,optCount)

    # Sort the data by the integer value
    mostUsed = dict(sorted(mostUsed.items(),key=lambda elem: elem[1],reverse=True))

    # Construct the menu to be printed to the user
    ui_Options = constr_opt(recUsed=recUsed, freqUsed=mostUsed, NoAddOption=AddInputs, optCount=optCount)

    # Print the options to the user
    pp.pprint(ui_Options)

    ui_list = list()

    # Collect first input
    ui = pyip.inputNum(prompt = "Please select a %s: " % inputTitle, greaterThan=0, lessThan=(len(ui_Options)+1))
    ui_list.append(ui_Options[ui-1])

    # Prompts the user for multiple inputs in the instance when needed
    while ui in range(2,(len(ui_Options)+1)) and AddInputs == True :
        ui = pyip.inputNum(prompt = "Please select another %s: " % inputTitle, greaterThan=0, lessThan=11)
        if ui != 1 and ui != (len(ui_Options)-1) : ui_list.append(ui_Options[ui-1])
        elif ui == (len(ui_Options)-1) : 
            other = pyip.inputStr(prompt="Please type desired %s: " % inputTitle, applyFunc=valididate_other)
            ui_list.append(other)

    return ui_list # Returns a list with all of the inputs


def test_Menu() :
    # Example Data
    mostFreqUsed = {'nprocshared=60' : 5, 'mem=60gb': 4, 'chk=__filename__.chk': 3, 'cpu=4' : 1, 'ssh=command' : 2, 'lindaworkers=(lina1,linda2,linda3)' : 1}
    mostRecUsed = Link0Keywords = ['nprocshared', 'oldraw=(__filename__,i8lab)', 'oldmatrix', 'lindaworkers', 'nproclinda', 'oldraw', 'oldmatrix=(__filename__,i8lab)', 'oldraw=(__filename__,i4lab)', 'chk', 'ssh=command', 'cpu', 'oldchk', 'oldmatrix=(__filename__,i4lab)', 'mem', 'gpucpu']
    title = "link0 input"

    # Implementation of function
    ui_list = Menu(freqUsed = mostFreqUsed, recUsed=mostRecUsed, inputTitle = title)
    print()
    pp.pprint(ui_list)


test_Menu()

# Data from scrape
allKeywords = ['admp', 'bd', 'bomd', 'cachesize', 'casscf', 'cbs', 'cbsextrapolate', 'ccd', 'charge', 'chkbasis', 'cid', 'cis', 'cndo', 'complex', 'constants', 'counterpoise', 'cphf', 'density', 'densityfit', 'dft', 'dftb', 'eet', 'eomccsd', 'ept', 'external', 'extrabasis', 'field', 'fmm', 'force', 'freq', 'gen', 'genchk', 'geom', 'gfinput', 'gfprint', 'gn', 'guess', 'gvb', 'hf', 'huckel', 'indo', 'integral', 'iop', 'irc', 'ircmax', 'link0', 'lsda', 'maxdisk', 'mindo3', 'mndo', 'mm', 'mp', 'name', 'nmr', 'oniom', 'optimization', 'output', 'pbc', 'polar', 'population', 'pressure', 'prop', 'pseudo', 'punch', 'qci', 'restart', 'sac-ci', 'scale', 'scan', 'scf', 'scrf', 'semi-empirical', 'sp', 'sparse', 'stable', 'symmetry', 'td', 'temperature', 'test', 'testmo', 'trackio', 'transformation', 'units', 'volume', 'w1', 'window', 'zindo']
Link0UserOpt = {'%nprocshared=60\n%mem=60gb\n': 5, '%nprocshared=4\n%mem=16gb\n': 5, 'custom': 5}
Link0Keywords = ['%nprocshared', '%oldraw=(__filename__,i8lab)', '%rwf', '%oldmatrix', '%lindaworkers', '%nproclinda', '#\xa0section', '%oldraw', '%oldmatrix=(__filename__,i8lab)', '%oldraw=(__filename__,i4lab)', '%chk', '%ssh=command', '%cpu', '%oldchk', '%oldmatrix=(__filename__,i4lab)', '%mem', '%gpucpu']