"""
UI.Menus.py contains the tools to collect user input from the command line and format it into a header or footer object 
"""

import pyinputplus as pyip
#from typing import List, Dict, Tuple

# Westmont Computational Chemistry ToolKit © 2022 by Riley Johnson, Curtis Barnhart is licensed under CC BY-NC-SA 4.0
# https://github.com/rijohnson2023/MOD
# http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1

def Menu1(data: 'dict[str:int]', inputTitle ="Input for list of strings"):
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
    # Sort the data dictionary
    # TUrn the top 4 options into a list
    UI_Choices = list(data.keys())
    UI_Choices.insert(0,"No additional inputs.")
    UI_Choices.append('Other:')
    UI_M1 = ''
    while UI_M1 != "No additional inputs." :
        UI_M1 = pyip.inputMenu(prompt="Set %s\n" % inputTitle, choices=UI_Choices, numbered=True, caseSensitive=False, )
        
    return UI_M1

def test_Menu1() :
    link0Data = {'nprocshared=60' : 5, 'mem=60gb': 4, 'chk=<filename>.chk': 3, 'cpu=4' : 1, 'ssh=command' : 2, 'lindaworkers=(lina1,linda2,linda3)' : 1}
    inputName = "link0 inputs"
    Menu1(data = link0Data, inputTitle = inputName)

test_Menu1()


def Menu2() :
    pass

def Menu3() :
    pass

allKeywords = ['admp', 'bd', 'bomd', 'cachesize', 'casscf', 'cbs', 'cbsextrapolate', 'ccd', 'charge', 'chkbasis', 'cid', 'cis', 'cndo', 'complex', 'constants', 'counterpoise', 'cphf', 'density', 'densityfit', 'dft', 'dftb', 'eet', 'eomccsd', 'ept', 'external', 'extrabasis', 'field', 'fmm', 'force', 'freq', 'gen', 'genchk', 'geom', 'gfinput', 'gfprint', 'gn', 'guess', 'gvb', 'hf', 'huckel', 'indo', 'integral', 'iop', 'irc', 'ircmax', 'link0', 'lsda', 'maxdisk', 'mindo3', 'mndo', 'mm', 'mp', 'name', 'nmr', 'oniom', 'optimization', 'output', 'pbc', 'polar', 'population', 'pressure', 'prop', 'pseudo', 'punch', 'qci', 'restart', 'sac-ci', 'scale', 'scan', 'scf', 'scrf', 'semi-empirical', 'sp', 'sparse', 'stable', 'symmetry', 'td', 'temperature', 'test', 'testmo', 'trackio', 'transformation', 'units', 'volume', 'w1', 'window', 'zindo']

Link0UserOpt = {'%nprocshared=60\n%mem=60gb\n': 5, '%nprocshared=4\n%mem=16gb\n': 5, 'custom': 5}

Link0Keywords = ['%nprocshared', '%oldraw=(FILENAME,i8lab)', '%rwf', '%oldmatrix', '%lindaworkers', '%nproclinda', '#\xa0section', '%oldraw', '%oldmatrix=(FILENAME,i8lab)', '%oldraw=(FILENAME,i4lab)', '%chk', '%ssh=command', '%cpu', '%oldchk', '%oldmatrix=(FILENAME,i4lab)', '%mem', '%gpucpu']

