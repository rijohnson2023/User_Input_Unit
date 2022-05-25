#!/opt/anaconda3/bin/env python
# MODIFIER : VERSION 1.0.3
#---------------------------------------------------------------------------------------
# Authors: Riley Johnson, Curtis Barnhart
# November 25, 2021
# This algorithm allows the user to define a single set of parameters for a Gaussian
# 16 test. It reads in Gaussian gjf and log files, is able to pull multiple basis sets
# from basis set exchange, and correctly format the data into a sinlge .gjf file. Output
# is printed to the user before saving. The user can either save to a new file, or write
# over the existing files. Currently it is fitted to prepare Single Point and Opt Freq
# tests. 
#---------------------------------------------------------------------------------------

import sys
import requests

###
## So, the idea here is to assign classes to InputGJF, InputLOG, and maybe more will come. But all inputs are going
## to be treated like databases. I want to be able to query certain contents of the files. I'm going to make them
## objects and then process them as those objects. The objects that exist so far are InputGJF and InputLOG. Future
## objects that might come up are Output_GJF, Output_QST2_GJF, Output_QST3_GJF, or other kinds of output. This is just to
## create a clear structure as the files get more complex and the tasks get more complex. It will also allow us to query
## different objects in the same way for certain objects. I.e. file.chargeMultCart will return the same values for both
## the InputGJF object and the InputLOG object, however, the program will understand that to get to those values will
## require some different workflows.
###

###
## The following functions are related to gathering the input from the user
###


##
# Collects the list of files to be edited from the commandline
# @ param : None
# @ return : List of files to be edited
def get_filenames() :
    argv = sys.argv[1:]
    return argv


##
# Collects the data block containing link0 and g16 commands or any additional commands for the gjf file. (To be concatenated in at the bottom of each file)
# @ param : None
# @ return: gjf footer as a string
def get_docInfo(docInfo) : 
    headerFooter = ""
    addLine = str(input("Construct the %s for each gjf file.\nWhen finished hit Enter to continue...\n\n" % docInfo )).lower()
    while addLine != "" :
        headerFooter += addLine + "\n"
        addLine = str(input()).lower()
    headerFooter += "\n"
    return headerFooter


##
# Collects the basis set names to be pulled from Basis Set Exchange. For the primary basis set, instead of having an atomic number
# list the string 'Primary' is included. This is because the primary atoms needs to be updated with each file. That function is 
# taken care of in BSE_metaBasisSet()
# @ param : None
# @ return: Dictionary containing the basis set name as the key, and the atoms for that basis set as the values
def get_basisSetName (basisSets = {}) :
    mult = s_input("\nWould you like to use multiple basis sets?\nAllowed answers are 'Y', 'N', 'Yes', or 'No' (case insensitive)\n")
    if mult in YES :
        basisSetName = s_input("\nWhat is the name of the primary basis set?\n", answers = BSE_VERSIONNUMBERS, mistake = "No basis set found in library.")
        primaryKey = basisSetName
        atoms = "Primary"
        while basisSetName != '' :
            basisSets[basisSetName] = atoms
            basisSetName = s_input("\nWhat is the name of the next basis set?\nEnter to continue...\n", answers = BSE_VERSIONNUMBERS, mistake = "No basis set found in library.",exception = '')
            if basisSetName != '' :
                atoms = s_input("\nWhat atoms will be run under this basis set? (case sensitive)\nDeliminate each atom with whitespace.\n", answers = PERIODICTABLE, mistake = "Atom not found in periodic table. Please re-enter %s: ",answer_type="Space Deliminated String").split()
                atoms = elemSymToAtomicNum(atoms) # Converting element symbols to atomic numbers
    else :
        basisSetName = s_input("\nPlease enter the name of the basis set for all files:\n",answers = BSE_VERSIONNUMBERS, mistake = "No basis set found in library.")
        basisSets[basisSetName] = "Primary"
        primaryKey = basisSetName
    return basisSets, primaryKey


##
# s_input sanitizes the input the user gives depending on what is specified by its arguments. 'question' is a string
# containing the question that is displayed to the user, answer_type is a string, either "str" or "Space Deliminated String", 
# which indicates what type of answer is expected of the user, and answers is either the list of acceptable string answers 
# (if a string is expected of the user) or a string containing the range of acceptable integers (if an integer is expected of 
# the user) that are expected of the user.
# @ param : Statement to print
# @ return: input
def s_input(question, answer_type="str", answers=('y', 'n', 'yes', 'no'), mistake = "You did not give an allowed answer. Please answer again.\n", exception = None) :

    if answer_type == "str" :  # If the expected answer is a string, the code within this 'if' is executed
        raw_input = input(question).lower()  # String answers by the user are case insensitive
        if exception == None :
            # While the user has not given a valid answer, asks them again
            while raw_input not in answers :
                raw_input = input(mistake + question).lower()
            sanitized_input = raw_input
        else :
            # While the user has not given a valid answer, asks them again
            while raw_input not in answers and raw_input != exception :  
                raw_input = input(mistake + question).lower()
            sanitized_input = raw_input

    elif answer_type == "Space Deliminated String" :
        raw_input = input(question) # String answer by the user is case sensitive
        raw_inputs_list = raw_input.split() # split string on whitespace
        for i in range(len(raw_inputs_list)) :
            # Print out error and request replacement if input not found in answers
            while raw_inputs_list[i] not in answers :
                raw_inputs_list[i] = input(mistake % raw_inputs_list[i])
        # When a valid answer is given, re-formats the input as a space deliminated string, and saves it in 'sanitized_input'
        sanitized_input = str(sorted(raw_inputs_list)).strip("[]").replace("'","").replace(","," ")

    return sanitized_input  # Returns either a string or, both guaranteed to be acceptable answers


###
## The following functions and classes are related to parsing the data for each type of input file.
###


##
# Takes in a list of atomic numbers and returns a new list in the same order with the corresponding element Symbols
# @ param : list of atomic numbers
# @ return: list of element symbols
def atomicNumToElemSym(atomicNumbers) :
    elementSymbols = [""]*len(atomicNumbers)
    for i in range(len(atomicNumbers)) :
        try :
            elementSymbol = PERIODICTABLE[atomicNumbers[i]]
        except IndexError :
            elementSymbol = "XX"
        elementSymbols[i] = elementSymbol
    return elementSymbols


##
# Takes in a list of element symbols and returns a new list in the same order with the corresponding atomic numbers
# @ param : list of element symbols
# @ return: list of atomic numbers
def elemSymToAtomicNum(elementSymbols) : 
    atomicNumbers = [""]*len(elementSymbols)
    for i in range(len(elementSymbols)) :
        if elementSymbols[i] in PERIODICTABLE :
            atomicNumber = PERIODICTABLE.index(elementSymbols[i])
        else :
            atomicNumber = "XX"
        atomicNumbers[i] = atomicNumber
    return atomicNumbers


class InputFile :
    ##
    # Exhaustively processes the data within a Gaussian gjf or log file
    # @ PARAM : self, filename
    # @ RETURN: None
    def __init__(self,filename) :
        # InputFile IS A GJF FILE
        if ".gjf" in filename :
            # Opening the file and creating a string of all the contents within the file
            text = ""
            with open(filename, "r") as file:
                text = file.read()
            # Splitting the Gaussian data along '\n\n' because large data strings are separated
            # by a blank line in Gaussian gjf files. The string in the 0th position is the link0
            # commands with the '# g16 InputFile line'. The string in the 1st position is the 'Title
            # Card Required' line. The string in the 2nd position includes the charge, 
            # multiplicity, and element symbols with their corresponding xyz coordingates. Anything
            # following the 2nd string is still captured, but the data varies. It could be the 
            # connectivity values, a basis set, or additional InputFiles.
            self._DATA = text.split("\n\n")
            self.CHARGEMULTCART = self._DATA[2] + "\n"
            # Splitting the second data string by whitespace results in a list with the charge in
            # the 0th position, multiplicity in the 1st position.
            self.CHARGE = self.CHARGEMULTCART.split()[0]
            self.MULTIPLICITY = self.CHARGEMULTCART.split()[1]
            # The first newline character appears after the string including the charge and multiplicity
            # numbers. Slicing everything up to the first newline character leaves the element symbols
            # with their corresponding xyz coordingates formatted as a string.
            self.XYZCOORD = self.CHARGEMULTCART[(self.CHARGEMULTCART.find("\n")+1):]
            # Splitting the XYZCOORD string by the newline character yields each element symbol 
            # with the corresponding cartesian coordinates in a single string. Therefore if that 
            # string is split by whitespace, the element symbol is in the 0th position. These
            # lines create both a set and list of the element symbols in the gjf file. 
            self.ELEMENTLIST = [line.split()[0] for line in self.XYZCOORD.rstrip("\n").split("\n")]
            self.ELEMENTSET = set(self.ELEMENTLIST)
            # These lines create both a set and list of the atomic numbers corresponding to the 
            # elements in the gjf file using the global function elemSymToAtomicNum().
            self.ATOMICNUMBERLIST = elemSymToAtomicNum(self.ELEMENTLIST)
            self.ATOMICNUMBERSET = set(self.ATOMICNUMBERLIST)
            self.OK = True

        # InputFile FILE IS A LOG FILE
        elif ".log" in filename :
            with open(filename) as file:
                # Reads through all data in the file
                self._DATA = file.readlines()
                self.CHARGE = None
                self.MULTIPLICITY = None 
                # Iterates over all the data
                for i, line in enumerate(self._DATA):
                    # Locates the cartesian, atomic number, and atomic symbol information in the data
                    if "Input orientation" in line or "Standard orientation" in line:
                        self.ATOMICNUMBERLIST = []
                        self.XYZ = []
                        self.INFILE = self._DATA[i+5:]
                        for j, line in enumerate(self.INFILE):
                            if "-------" in line :
                                break
                            self.ATOMICNUMBERLIST.append(int(line.split()[1]))
                            if len(line.split()) > 5:
                                self.XYZ.append([float(line.split()[3]),float(line.split()[4]),float(line.split()[5])])
                            else:
                                self.XYZ.append([float(line.split()[2]),float(line.split()[3]),float(line.split()[4])])
                    # Locates the charge and multiplicity information in the data
                    if "Charge" in line.strip() and "Multiplicity" in line.strip():
                        self.CHARGE = line.strip("=").split()[2]
                        self.MULTIPLICITY = line.strip('=').split()[5]
                # Creates a list of all the element symbols corresponding to the elements found in the file.
                self.ELEMENTLIST = atomicNumToElemSym(self.ATOMICNUMBERLIST)
                # Writes a single formatted string with the atom symbol, and cartesian coordinates. Depending on the 
                # length of the string containing the Atom Symbol, the x coordinate spacing is appropriately changed.
                self.XYZCOORD =''
                for atom, xyz in zip(self.ELEMENTLIST, self.XYZ):
                    if len(atom) == 1 :
                        self.XYZCOORD += " {0} {1:27.8f} {2:13.8f} {3:13.8f}\n".format(atom, *xyz)
                    elif len(atom) == 2 :
                        self.XYZCOORD += " {0} {1:26.8f} {2:13.8f} {3:13.8f}\n".format(atom, *xyz)
                    elif len(atom) == 3 :
                        self.XYZCOORD += " {0} {1:25.8f} {2:13.8f} {3:13.8f}\n".format(atom, *xyz)
                # Correctly formats the charge and multiplicity values into the CHARGEMULTCART data structure
                self.CHARGEMULTCART = "{0} {1}\n{2}".format(self.CHARGE, self.MULTIPLICITY, self.XYZCOORD)
                if len(self.CHARGE) == 1 :
                    self.CHARGEMULTCART.replace(self.CHARGE," %s" % self.CHARGE)
            # Creating a set of the Element Symbols and the corresponding Atomic Numbers
            self.ELEMENTSET = set(self.ELEMENTLIST)
            self.ATOMICNUMBERSET = set(self.ATOMICNUMBERLIST)
            self.OK = True
        else :
            self.OK = False


    ##
    # @ param : self
    # @ return: The string including the charge, multiplicity, and element symbols with their
    # corresponding xyz coordingates from the gjf file.
    def ok(self) :
        return self.OK


    ##
    # @ param : self
    # @ return: The string including the charge, multiplicity, and element symbols with their
    # corresponding xyz coordingates from the gjf file.
    def cmc(self) :
        return self.CHARGEMULTCART


    ##
    # @ param : self
    # @ return: The charge of the structure in the gjf file.
    def charge(self) :
        return self.CHARGE


    ##
    # @ param : self
    # @ return: The multiplicity of the structure in the gjf file.
    def mult(self) :
        return self.MULTIPLICITY


    ##
    # @ param : self
    # @ return: the string including the element symbols with their corresponding cartesian
    # coordingates from the gjf file.
    def xyz(self) :
        return self.XYZCOORD


    ##
    # @ param : self
    # @ return: a list containing every element symbol in the gjf file.
    def elementList(self) :
        # NOTE: The element symbols in the list are in the same order from left to right as 
        # the element symbols in the XYZCOORD moving from top to bottom.
        return self.ELEMENTLIST


    ##
    # @ param : self
    # @ return: a set containing element symbols in the gjf file
    def elementSet(self) :
        return self.ELEMENTSET


    ##
    # @ param : self
    # @ return: a list containing every atomic number for each element in the gjf file
    def atomNumList(self) :
        # NOTE: The order of the atomic numbers are in the same order from left to right as 
        # the element symbols in the XYZCOORD moving from top to bottom. 
        return self.ATOMICNUMBERLIST

    ##
    # @ param : self
    # @ return: a set containing the atomic numbers for the elements in the gjf file
    def atomNumSet(self) :
        return self.ATOMICNUMBERSET


###
## The following functions are all related to constructing the data structures for the output files.
###


##
# Locates the string "geom=connectivity" and removes it if present. Adds Gaussian keyword "gen" if not preset
# @ param : header
# @ return: correctly formatted header
def removeConnectivity (header) :
    if "geom=connectivity" in header :
        newHeader = header.replace(" geom=connectivity","")
    else :
        newHeader = header
    return newHeader


##
# Locats the string "%chk" and determines the length of the line. Removes the entire line and replaces it 
# with the appropriate .chk reference file
# @ param : filename and header
# @ return: correctly formatted header
def write_chk_line (filename,header) :
    if "%chk" in header :
        chkfilename = filename[:-4] + ".chk"
        oldChkStr = ""
        # Locates the str with %chk
        x = header.find("%chk")
        y = header.find("\n",x)
        # Reconstructs the old str
        oldChkStr = header[x: y]
        # Replaces old chkline with newChkStr
        newChkStr = "%chk=" + chkfilename
        newHeader = header.replace(oldChkStr,newChkStr)
    else :
        newHeader = header
    return newHeader


##
# Pulls the basis set from Basis Set Exchange. Deletes the header so only the basis set remains
# @ param : url, key (Basis Set name), atomStr (list of atoms formatted as a string for the specific Basis Set.)
# @ return: Basis Set from Basis Set Exchange
def BSE_webRequest(key, basisSetNames) :
    # Creates a sting of the atomic numbers for the Basis Set Exchange url
    atomStr = str(sorted(basisSetNames[key])).strip("[]").replace(" ", "")
    # Attempts to grab the version number from the Basis Set Excahnge Dictionary. The version number identifies whether the basis set is stored
    # on the old basis set exhange or the new one.
    try :
        version = str(BSE_VERSIONNUMBERS[key])
    except KeyError:
        print("%s not found in basis set library" % key)
        # Does not really catch error. Error is caught when the WebRequest fails.
        # Typically these errors will be on our end. The basis set dictionary needs
        # is bug free yet.
        version = 0
    # Concatenates pieces for the Basis Set Exchange url
    url = 'https://www.basissetexchange.org/download_basis/basis/' + key + '/format/gaussian94/?version=' + version + '&elements=' + atomStr
    response = requests.get(url)
    if response.status_code == requests.codes.ok :
        # separates the Basis Set Exchange title from the actual basis set.
        basisSet = response.text.split("\n\n")[1].rstrip()
        # Grabs ECP and other information if present
        if len(response.text.split("\n\n")) > 2 :
            # basisSet += "\n\n" + response.text.split("\n\n")[2].rstrip()
            raw_bs = response.text.split("\n\n")[2:]
            for i in range(len(raw_bs)) :
                basisSet += "\n\n" + raw_bs[i]
            basisSet.strip()
    else :
        elemStr = str(atomicNumToElemSym(sorted(basisSetNames[key]))).strip("[]").replace("'", "")
        basisSet = "\n%s 0\n%s\n****" % (elemStr.replace(","," "), key)
    return basisSet


##
# Takes in a set of atomic numbers and the basis set name, opens web url. Pulls related basis set from BSE.
# @ param : basis set name and sorted list of atomic numbers
# @ return: corresponding basis set formated as a string
def BSE_metaBasisSet(basisSetNames,primaryKey,atomicNumbers) :
    primaryElements = atomicNumbers
    # Removes elements that will not be under the primary basis set
    for key in basisSetNames :
        if isinstance(basisSetNames[key],list) : 
            primaryElements = atomicNumbers.difference(set(basisSetNames[key]))
    # Replaces key value 'Primary' with the list of atoms for the primary basis set 
    basisSetNames[primaryKey] = primaryElements
    # Downloads the basis sets for each set of atoms
    basisSet = BSE_webRequest(primaryKey, basisSetNames)
    # Removes the primary key from the dictionary
    basisSetNames.pop(primaryKey)
    # Iterates over the rest of the basis sets and atomlists and constructs a basis set
    if len(basisSetNames) > 0 :
        for key in basisSetNames :
            basisSet += BSE_webRequest(key, basisSetNames)
    basisSet += "\n\n"
    return basisSet


##
# Edits every single file, pulling the information needed from the contents formated as a gjf file and stitching together a string of contents ready for g16
# @ param : filename as str, header as str, basis set name as str, and footer as str.
# @ return: str with content for the outfile
def prepOutfile(filename,basisSetName,primaryKey,header,footer) :
    # Identifies the type of file
    query = InputFile(filename)
    if not query.ok() :
        print("Not Processing %s" % filename)
        return None
    
    print("Processing %s" % filename)
    # Inserts the correct filename for the .chk file line
    gjfHeader = write_chk_line(filename,header)

    # Pulls the basis set from Basis Set Exchange
    basis_set = BSE_metaBasisSet(basisSetName, primaryKey, query.atomNumSet())

    # Concatenates the correct strings for the jon into a single string
    outfile = gjfHeader + "Title Card Required\n\n" + query.cmc() + basis_set + footer
    # Removes unnecessary whitespace at the end of the file.
    outfile = outfile.rstrip() + "\n\n"

    # Saves the new contents for the .gjf files in a dictionary with the filename as the key.
    return outfile


##
# Prints out the contents of each file to the console for the user to proof-read. Gives the option to save or discard the changes.
# @ param : list of files, dictionary of new contents
# @ return: None
def saveView(fileList,fileExtension,newContentsDict) :
    i = 0
    view = "y"
    # initializes while loop that prints out the new contents for each file
    while view in YES:
        if view in YES :
            print("-"*60)
            print(newContentsDict[fileList[i]])
            outFile = fileList[i][:len(fileList[i])-4] + fileExtension + ".gjf"
        save = s_input("Would you like to save the following file: %s\nAllowed answers are 'Yes', 'Y', 'No', 'N' (case insensitive)\n" % outFile)
        if save in YES :
            with open(outFile, "w") as file:
                file.write(newContentsDict[fileList[i]])
        i += 1
        if len(newContentsDict) > 1 and i <= len(fileList):
            view = s_input("Would you like to see the rest of the files?\nAllowed answers are 'Yes', 'Y', 'No', 'N' (case insensitive)\n")
        else :
            view = "n"
    # if the user does not wish to see the rest of the files, still gives opportunity to save data.
    if len(newContentsDict) > 1 and i <= len(fileList) :
        save = s_input("Would you like to save the rest of the files?\nAllowed answers are 'Yes', 'Y', 'No', 'N' (case insensitive)\n")
        if save in YES :
            for j in range(i, len(fileList)) :
                outFile = fileList[j][:len(fileList[j])-4] + fileExtension + ".gjf"
                with open(outFile, "w") as file:
                    file.write(newContentsDict[fileList[j]])
                j += 1
    return


##
def main() :
    # Collects the list of files to be editied
    fileList=get_filenames()
    # Collects all of the necessary input for the file preparation
    header = removeConnectivity(get_docInfo("header")) # header is case insenstitive
    basisSetName, primaryKey =get_basisSetName()
    print("")
    footer = get_docInfo("footer") # footer is case insensitive
    newExtension = s_input("Would you like to output new contents to files with a flag at the end of the filename?\n")
    if newExtension in YES :
        file_ext = input("Please enter the flag for the end of the filename:\n")
    else :
        file_ext = ''
    # Notifies the user that the program is working
    print("-"*50)
    print("Relax, it's working")
    print("-"*50)
    # Runs the functions which iterate over all of the files in the filelist, format the data, and
    # asks the user if they wish to save it.
    outfileDict = {}
    notEdited = list()
    for file in fileList :
        outContents = prepOutfile(file,basisSetName,primaryKey,header,footer)
        if outContents == None :
            notEdited.append(file)
            fileList.remove(file)
        else :
            outfileDict[file] = outContents
    saveView(fileList,file_ext,outfileDict)
    if len(notEdited) > 0 :
        print("-"*50)
        print("The following file(s) were not edited:")
        for file in notEdited :
            print(file)
        print("-"*50)
    #info() # prints out the current parameters for the funcion. Need to initialize flag.


# Radii used to determine connectivity in symmetry corrections
# Covalent radii taken from Cambridge Structural Database 
RADII = {'H' :0.32, 'He':0.93, 'Li':1.23, 'Be':0.90, 'B' :0.82, 'C' :0.77, 'N' :0.75, 'O' :0.73, 'F' :0.72, 'Ne':0.71, 'Na':1.54, 'Mg':1.36, 'Al':1.18, 'Si':1.11, 'P' :1.06, 'S' :1.02, 'Cl':0.99, 'Ar':0.98, 'K' :2.03, 'Ca':1.74, 'Sc':1.44, 'Ti':1.32, 'V' :1.22, 'Cr':1.18, 'Mn':1.17, 'Fe':1.17, 'Co':1.16, 'Ni':1.15, 'Cu':1.17, 'Zn':1.25, 'Ga':1.26, 'Ge':1.22, 'As':1.20, 'Se':1.16, 'Br':1.14, 'Kr':1.12, 'Rb':2.16, 'Sr':1.91, 'Y' :1.62, 'Zr':1.45, 'Nb':1.34, 'Mo':1.30, 'Tc':1.27, 'Ru':1.25, 'Rh':1.25, 'Pd':1.28, 'Ag':1.34, 'Cd':1.48, 'In':1.44, 'Sn':1.41, 'Sb':1.40, 'Te':1.36, 'I' :1.33, 'Xe':1.31, 'Cs':2.35, 'Ba':1.98, 'La':1.69, 'Lu':1.60, 'Hf':1.44, 'Ta':1.34, 'W' :1.30, 'Re':1.28, 'Os':1.26, 'Ir':1.27, 'Pt':1.30, 'Au':1.34, 'Hg':1.49, 'Tl':1.48, 'Pb':1.47, 'Bi':1.46, 'X' :0}

# Periodic Table of Elements, the index number is the atomic number
PERIODICTABLE = ["", "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Uub", "Uut", "Uuq", "Uup", "Uuh", "Uus", "Uuo"]

# Dictionary with every available basis set on basis set exchange. Basis set name is the key, the version number is the value assigned to each key
#BSE_VERSIONNUMBERS = {'2ZaPa-NR-CV': 1, '2ZaPa-NR': 1, '3-21G': 1, '3ZaPa-NR-CV': 1, '3ZaPa-NR': 1, '4-31G': 1, '4ZaPa-NR-CV': 1, '4ZaPa-NR': 1, '5-21G': 1, '5ZaPa-NR-CV': 1, '5ZaPa-NR': 1, '6-21G': 1, '6-31++G': 1, '6-31++G*': 1, '6-31++G**-J': 0, '6-31++G**': 1, '6-31+G': 1, '6-31+G*-J': 0, '6-31+G*': 1, '6-31+G**': 1, '6-311++G(2d,2p)': 0, '6-311++G(3df,3pd)': 0, '6-311++G': 0, '6-311++G*': 0, '6-311++G**-J': 0, '6-311++G**': 0, '6-311+G(2d,p)': 0, '6-311+G': 0, '6-311+G*-J': 0, '6-311+G*': 0, '6-311+G**': 0, '6-311G(2df,2pd)': 0, '6-311G(d,p)': 0, '6-311G-J': 0, '6-311G': 0, '6-311G*': 0, '6-311G**-RIFIT': 1, '6-311G**': 0, '6-311xxG(d,p)': 1, '6-31G(2df,p)': 0, '6-31G(3df,3pd)': 0, '6-31G(d,p)': 1, '6-31G-Blaudeau': 0, '6-31G-J': 0, '6-31G': 1, '6-31G*-Blaudeau': 0, '6-31G*': 1, '6-31G**-RIFIT': 1, '6-31G**': 1, '6ZaPa-NR': 1, '7ZaPa-NR': 1, 'acv2z-J': 1, 'acv3z-J': 1, 'acv4z-J': 1, 'admm-1': 1, 'admm-2': 1, 'admm-3': 1, 'AHGBS-5': 1, 'AHGBS-7': 1, 'AHGBS-9': 1, 'AHGBSP1-5': 1, 'AHGBSP1-7': 1, 'AHGBSP1-9': 1, 'AHGBSP2-5': 1, 'AHGBSP2-7': 1, 'AHGBSP2-9': 1, 'AHGBSP3-5': 1, 'AHGBSP3-7': 1, 'AHGBSP3-9': 1, 'Ahlrichs pVDZ': 0, 'Ahlrichs TZV': 0, 'Ahlrichs VDZ': 0, 'Ahlrichs VTZ': 0, 'ANO-DK3': 1, 'ANO-R': 2, 'ANO-R0': 2, 'ANO-R1': 2, 'ANO-R2': 2, 'ANO-R3': 2, 'ANO-RCC-MB': 1, 'ANO-RCC-VDZ': 1, 'ANO-RCC-VDZP': 1, 'ANO-RCC-VQZP': 1, 'ANO-RCC-VTZ': 1, 'ANO-RCC-VTZP': 1, 'ANO-RCC': 1, 'ANO-VT-DZ': 1, 'ANO-VT-QZ': 2, 'ANO-VT-TZ': 1, 'apr-cc-pV(Q+d)Z': 0, 'ATZP-ZORA': 1, 'aug-admm-1': 1, 'aug-admm-2': 1, 'aug-admm-3': 1, 'aug-cc-pCV5Z': 0, 'aug-cc-pCVDZ-DK': 0, 'aug-cc-pCVDZ': 0, 'aug-cc-pCVQZ-DK': 0, 'aug-cc-pCVQZ': 0, 'aug-cc-pCVTZ-DK': 0, 'aug-cc-pCVTZ': 0, 'aug-cc-pV(5+d)Z': 1, 'aug-cc-pV(D+d)Z': 1, 'aug-cc-pV(Q+d)Z': 1, 'aug-cc-pV(T+d)Z': 1, 'aug-cc-pV5Z-DK': 0, 'aug-cc-pV5Z-OPTRI': 0, 'aug-cc-pV5Z-PP-OPTRI': 0, 'aug-cc-pV5Z-PP-RIFIT': 0, 'aug-cc-pV5Z-PP': 0, 'aug-cc-pV5Z-RIFIT': 1, 'aug-cc-pV5Z': 1, 'aug-cc-pV6Z-RIFIT': 1, 'aug-cc-pV6Z': 1, 'aug-cc-pV7Z': 0, 'aug-cc-pVDZ-DK': 0, 'aug-cc-pVDZ-DK3': 1, 'aug-cc-pVDZ-OPTRI': 0, 'aug-cc-pVDZ-PP-OPTRI': 0, 'aug-cc-pVDZ-PP-RIFIT': 0, 'aug-cc-pVDZ-PP': 0, 'aug-cc-pVDZ-RIFIT': 1, 'aug-cc-pVDZ-X2C': 1, 'aug-cc-pVDZ': 1, 'aug-cc-pVQZ-DK': 0, 'aug-cc-pVQZ-DK3': 1, 'aug-cc-pVQZ-OPTRI': 0, 'aug-cc-pVQZ-PP-OPTRI': 0, 'aug-cc-pVQZ-PP-RIFIT': 0, 'aug-cc-pVQZ-PP': 0, 'aug-cc-pVQZ-RIFIT': 1, 'aug-cc-pVQZ-X2C': 1, 'aug-cc-pVQZ': 1, 'aug-cc-pVTZ-DK': 0, 'aug-cc-pVTZ-DK3': 1, 'aug-cc-pVTZ-J': 0, 'aug-cc-pVTZ-OPTRI': 0, 'aug-cc-pVTZ-PP-OPTRI': 0, 'aug-cc-pVTZ-PP-RIFIT': 0, 'aug-cc-pVTZ-PP': 0, 'aug-cc-pVTZ-RIFIT': 1, 'aug-cc-pVTZ-X2C': 1, 'aug-cc-pVTZ': 1, 'aug-cc-pwCV5Z-DK': 0, 'aug-cc-pwCV5Z-PP-OPTRI': 0, 'aug-cc-pwCV5Z-PP-RIFIT': 0, 'aug-cc-pwCV5Z-PP': 0, 'aug-cc-pwCV5Z-RIFIT': 1, 'aug-cc-pwCV5Z': 0, 'aug-cc-pwCVDZ-DK3': 1, 'aug-cc-pwCVDZ-PP-OPTRI': 0, 'aug-cc-pwCVDZ-PP-RIFIT': 0, 'aug-cc-pwCVDZ-PP': 0, 'aug-cc-pwCVDZ-RIFIT': 1, 'aug-cc-pwCVDZ-X2C': 1, 'aug-cc-pwCVDZ': 0, 'aug-cc-pwCVQZ-DK': 0, 'aug-cc-pwCVQZ-DK3': 1, 'aug-cc-pwCVQZ-PP-OPTRI': 0, 'aug-cc-pwCVQZ-PP-RIFIT': 0, 'aug-cc-pwCVQZ-PP': 0, 'aug-cc-pwCVQZ-RIFIT': 1, 'aug-cc-pwCVQZ-X2C': 1, 'aug-cc-pwCVQZ': 0, 'aug-cc-pwCVTZ-DK': 0, 'aug-cc-pwCVTZ-DK3': 1, 'aug-cc-pwCVTZ-PP-OPTRI': 0, 'aug-cc-pwCVTZ-PP-RIFIT': 0, 'aug-cc-pwCVTZ-PP': 0, 'aug-cc-pwCVTZ-RIFIT': 1, 'aug-cc-pwCVTZ-X2C': 1, 'aug-cc-pwCVTZ': 0, 'aug-ccX-5Z': 1, 'aug-ccX-DZ': 1, 'aug-ccX-QZ': 1, 'aug-ccX-TZ': 1, 'aug-mcc-pV5Z': 0, 'aug-mcc-pV6Z': 0, 'aug-mcc-pV7Z': 0, 'aug-mcc-pV8Z': 0, 'aug-mcc-pVQZ': 0, 'aug-mcc-pVTZ': 0, 'aug-pc-0': 0, 'aug-pc-1': 0, 'aug-pc-2': 0, 'aug-pc-3': 0, 'aug-pc-4': 0, 'aug-pcH-1': 1, 'aug-pcH-2': 1, 'aug-pcH-3': 1, 'aug-pcH-4': 1, 'aug-pcJ-0': 1, 'aug-pcJ-0_2006': 0, 'aug-pcJ-1': 1, 'aug-pcJ-1_2006': 0, 'aug-pcJ-2': 1, 'aug-pcJ-2_2006': 0, 'aug-pcJ-3': 1, 'aug-pcJ-3_2006': 0, 'aug-pcJ-4': 1, 'aug-pcJ-4_2006': 0, 'aug-pcS-0': 0, 'aug-pcS-1': 0, 'aug-pcS-2': 0, 'aug-pcS-3': 0, 'aug-pcS-4': 0, 'aug-pcseg-0': 1, 'aug-pcseg-1': 1, 'aug-pcseg-2': 1, 'aug-pcseg-3': 1, 'aug-pcseg-4': 1, 'aug-pcSseg-0': 1, 'aug-pcSseg-1': 1, 'aug-pcSseg-2': 1, 'aug-pcSseg-3': 1, 'aug-pcSseg-4': 1, 'aug-pcX-1': 1, 'aug-pcX-2': 1, 'aug-pcX-3': 1, 'aug-pcX-4': 1, 'aug-pV7Z': 0, 'binning 641(d)': 0, 'binning 641(df)': 0, 'binning 641+(d)': 0, 'binning 641+(df)': 0, 'binning 641+': 0, 'binning 641': 0, 'binning 962(d)': 0, 'binning 962(df)': 0, 'binning 962+(d)': 0, 'binning 962+(df)': 0, 'binning 962+': 0, 'binning 962': 0, 'cc-pCV5Z': 0, 'cc-pCVDZ-DK': 0, 'cc-pCVDZ-F12-OPTRI': 0, 'cc-pCVDZ-F12-RIFIT': 0, 'cc-pCVDZ-F12': 0, 'cc-pCVDZ': 0, 'cc-pCVQZ-DK': 0, 'cc-pCVQZ-F12-OPTRI': 0, 'cc-pCVQZ-F12-RIFIT': 0, 'cc-pCVQZ-F12': 0, 'cc-pCVQZ': 0, 'cc-pCVTZ-DK': 0, 'cc-pCVTZ-F12-OPTRI': 0, 'cc-pCVTZ-F12-RIFIT': 0, 'cc-pCVTZ-F12': 0, 'cc-pCVTZ': 0, 'cc-pV(5+d)Z': 1, 'cc-pV(D+d)Z': 1, 'cc-pV(Q+d)Z': 1, 'cc-pV(T+d)Z': 1, 'cc-pV5Z(fi/sf/fw)': 0, 'cc-pV5Z(fi/sf/lc)': 0, 'cc-pV5Z(fi/sf/sc)': 0, 'cc-pV5Z(pt/sf/fw)': 0, 'cc-pV5Z(pt/sf/lc)': 0, 'cc-pV5Z(pt/sf/sc)': 0, 'cc-pV5Z-DK': 0, 'cc-pV5Z-F12(rev2)': 1, 'cc-pV5Z-F12': 1, 'cc-pV5Z-JKFIT': 1, 'cc-pV5Z-PP-RIFIT': 0, 'cc-pV5Z-PP': 0, 'cc-pV5Z-RIFIT': 1, 'cc-pV5Z': 1, 'cc-pV6Z-RIFIT': 1, 'cc-pV6Z': 1, 'cc-pV8Z': 0, 'cc-pV9Z': 0, 'cc-pVDZ(fi/sf/fw)': 0, 'cc-pVDZ(fi/sf/lc)': 0, 'cc-pVDZ(fi/sf/sc)': 0, 'cc-pVDZ(pt/sf/fw)': 0, 'cc-pVDZ(pt/sf/lc)': 0, 'cc-pVDZ(pt/sf/sc)': 0, 'cc-pVDZ(seg-opt)': 0, 'cc-pVDZ-DK': 0, 'cc-pVDZ-DK3': 1, 'cc-pVDZ-F12(rev2)': 1, 'cc-pVDZ-F12-OPTRI': 0, 'cc-pVDZ-F12': 0, 'cc-pVDZ-PP-RIFIT': 0, 'cc-pVDZ-PP': 0, 'cc-pVDZ-RIFIT': 1, 'cc-pVDZ-X2C': 1, 'cc-pVDZ': 1, 'cc-pVQZ(fi/sf/fw)': 0, 'cc-pVQZ(fi/sf/lc)': 0, 'cc-pVQZ(fi/sf/sc)': 0, 'cc-pVQZ(pt/sf/fw)': 0, 'cc-pVQZ(pt/sf/lc)': 0, 'cc-pVQZ(pt/sf/sc)': 0, 'cc-pVQZ(seg-opt)': 0, 'cc-pVQZ-DK': 0, 'cc-pVQZ-DK3': 1, 'cc-pVQZ-F12(rev2)': 1, 'cc-pVQZ-F12-OPTRI': 0, 'cc-pVQZ-F12': 0, 'cc-pVQZ-JKFIT': 1, 'cc-pVQZ-PP-RIFIT': 0, 'cc-pVQZ-PP': 0, 'cc-pVQZ-RIFIT': 1, 'cc-pVQZ-X2C': 1, 'cc-pVQZ': 1, 'cc-pVTZ(fi/sf/fw)': 0, 'cc-pVTZ(fi/sf/lc)': 0, 'cc-pVTZ(fi/sf/sc)': 0, 'cc-pVTZ(pt/sf/fw)': 0, 'cc-pVTZ(pt/sf/lc)': 0, 'cc-pVTZ(pt/sf/sc)': 0, 'cc-pVTZ(seg-opt)': 0, 'cc-pVTZ-DK': 0, 'cc-pVTZ-DK3': 1, 'cc-pVTZ-F12(rev2)': 1, 'cc-pVTZ-F12-OPTRI': 0, 'cc-pVTZ-F12': 0, 'cc-pVTZ-JKFIT': 1, 'cc-pVTZ-PP-RIFIT': 0, 'cc-pVTZ-PP': 0, 'cc-pVTZ-RIFIT': 1, 'cc-pVTZ-X2C': 1, 'cc-pVTZ': 1, 'cc-pwCV5Z-DK': 0, 'cc-pwCV5Z-PP-RIFIT': 0, 'cc-pwCV5Z-PP': 0, 'cc-pwCV5Z-RIFIT': 1, 'cc-pwCV5Z': 0, 'cc-pwCVDZ-DK3': 1, 'cc-pwCVDZ-PP-RIFIT': 0, 'cc-pwCVDZ-PP': 0, 'cc-pwCVDZ-RIFIT': 1, 'cc-pwCVDZ-X2C': 1, 'cc-pwCVDZ': 0, 'cc-pwCVQZ-DK': 0, 'cc-pwCVQZ-DK3': 2, 'cc-pwCVQZ-PP-RIFIT': 0, 'cc-pwCVQZ-PP': 0, 'cc-pwCVQZ-RIFIT': 1, 'cc-pwCVQZ-X2C': 1, 'cc-pwCVQZ': 0, 'cc-pwCVTZ-DK': 0, 'cc-pwCVTZ-DK3': 1, 'cc-pwCVTZ-PP-RIFIT': 0, 'cc-pwCVTZ-PP': 0, 'cc-pwCVTZ-RIFIT': 1, 'cc-pwCVTZ-X2C': 1, 'cc-pwCVTZ': 0, 'ccemd-2': 0, 'ccemd-3': 0, 'ccJ-pV5Z': 0, 'ccJ-pVDZ': 0, 'ccJ-pVQZ': 0, 'ccJ-pVTZ': 0, 'ccX-5Z': 1, 'ccX-DZ': 1, 'ccX-QZ': 1, 'ccX-TZ': 1, 'coemd-2': 0, 'coemd-3': 0, 'coemd-4': 0, 'coemd-ref': 0, 'Cologne DKH2': 0, 'CRENBL ECP': 0, 'CRENBL': 0, 'CRENBS ECP': 0, 'CRENBS': 0, 'd-aug-cc-pV5Z': 0, 'd-aug-cc-pV6Z': 0, 'd-aug-cc-pVDZ': 0, 'd-aug-cc-pVQZ': 0, 'd-aug-cc-pVTZ': 0, 'def2-ECP': 1, 'def2-QZVP-RIFIT': 1, 'def2-QZVP': 1, 'def2-QZVPD': 1, 'def2-QZVPP-RIFIT': 1, 'def2-QZVPP': 1, 'def2-QZVPPD-RIFIT': 1, 'def2-QZVPPD': 1, 'def2-SV(P)-JKFIT': 1, 'def2-SV(P)-RIFIT': 1, 'def2-SV(P)': 1, 'def2-SVP-RIFIT': 1, 'def2-SVP': 1, 'def2-SVPD-RIFIT': 1, 'def2-SVPD': 1, 'def2-TZVP-RIFIT': 1, 'def2-TZVP': 1, 'def2-TZVPD-RIFIT': 1, 'def2-TZVPD': 1, 'def2-TZVPP-RIFIT': 1, 'def2-TZVPP': 1, 'def2-TZVPPD-RIFIT': 1, 'def2-TZVPPD': 1, 'def2-universal-JFIT': 1, 'def2-universal-JKFIT': 1, 'deMon2k-DZVP-GGA': 1, 'DFO+-NRLMOL': 1, 'DFO-1-BHS': 1, 'DFO-1': 1, 'DFO-2': 1, 'DFO-NRLMOL': 1, 'dgauss-a1-dftjfit': 0, 'dgauss-a1-dftxfit': 0, 'dgauss-a2-dftjfit': 0, 'dgauss-a2-dftxfit': 0, 'dgauss-dzvp': 0, 'dgauss-dzvp2': 0, 'dgauss-tzvp': 0, 'dhf-ECP': 0, 'dhf-QZVP': 0, 'dhf-QZVPP': 0, 'dhf-SV(P)': 0, 'dhf-SVP': 0, 'dhf-TZVP': 0, 'dhf-TZVPP': 0, 'DZ (Dunning-Hay)': 0, 'DZ + Double Rydberg (Dunning-Hay)': 0, 'DZ + Rydberg (Dunning-Hay)': 0, 'DZP (Dunning-Hay)': 0, 'DZP + Diffuse (Dunning-Hay)': 0, 'DZP + Rydberg (Dunning-Hay)': 0, 'FANO-5Z': 1, 'FANO-6Z': 1, 'FANO-DZ': 1, 'FANO-QZ': 1, 'FANO-TZ': 1, 'HGBS-5': 1, 'HGBS-7': 1, 'HGBS-9': 1, 'HGBSP1-5': 1, 'HGBSP1-7': 1, 'HGBSP1-9': 1, 'HGBSP2-5': 1, 'HGBSP2-7': 1, 'HGBSP2-9': 1, 'HGBSP3-5': 1, 'HGBSP3-7': 1, 'HGBSP3-9': 1, 'IGLO-II': 0, 'IGLO-III': 0, 'jgauss-dzp': 1, 'jgauss-qz2p': 1, 'jgauss-qzp': 1, 'jgauss-tzp1': 1, 'jgauss-tzp2': 1, 'jorge-5ZP-DKH': 1, 'jorge-5ZP': 1, 'jorge-6ZP-DKH': 1, 'jorge-6ZP': 1, 'jorge-A5ZP': 1, 'jorge-ADZP': 1, 'jorge-AQZP': 1, 'jorge-ATZP': 1, 'jorge-DZP-DKH': 1, 'jorge-DZP': 1, 'jorge-QZP-DKH': 1, 'jorge-QZP': 1, 'jorge-TZP-DKH': 1, 'jorge-TZP': 1, 'jul-cc-pV(D+d)Z': 0, 'jul-cc-pV(Q+d)Z': 0, 'jul-cc-pV(T+d)Z': 0, 'jun-cc-pV(D+d)Z': 0, 'jun-cc-pV(Q+d)Z': 0, 'jun-cc-pV(T+d)Z': 0, 'Koga unpolarized': 1, 'LANL08(d)': 0, 'LANL08(f)': 0, 'LANL08+': 0, 'LANL08': 0, 'LANL2DZ ECP': 0, 'LANL2DZ': 0, 'LANL2DZdp': 0, 'LANL2TZ(f)': 0, 'LANL2TZ+': 0, 'LANL2TZ': 0, 'm6-31G': 0, 'm6-31G*': 0, 'maug-cc-pV(D+d)Z': 0, 'maug-cc-pV(Q+d)Z': 0, 'maug-cc-pV(T+d)Z': 0, 'may-cc-pV(Q+d)Z': 0, 'may-cc-pV(T+d)Z': 0, 'MIDI!': 1, 'MIDI': 0, 'MIDIX': 1, 'MINI': 0, 'modified-LANL2DZ': 0, 'NASA Ames ANO': 0, 'NASA Ames ANO2': 0, 'NASA Ames cc-pCV5Z': 0, 'NASA Ames cc-pCVQZ': 0, 'NASA Ames cc-pCVTZ': 0, 'NASA Ames cc-pV5Z': 0, 'NASA Ames cc-pVQZ': 0, 'NASA Ames cc-pVTZ': 0, 'NLO-V': 0, 'NMR-DKH (TZ2P)': 0, 'ORP': 1, 'Partridge Uncontracted 1': 0, 'Partridge Uncontracted 2': 0, 'Partridge Uncontracted 3': 0, 'Partridge Uncontracted 4': 0, 'pc-0': 0, 'pc-1': 0, 'pc-2': 0, 'pc-3': 0, 'pc-4': 0, 'pcemd-2': 0, 'pcemd-3': 0, 'pcemd-4': 0, 'pcH-1': 1, 'pcH-2': 1, 'pcH-3': 1, 'pcH-4': 1, 'pcJ-0': 1, 'pcJ-0_2006': 0, 'pcJ-1': 1, 'pcJ-1_2006': 0, 'pcJ-2': 1, 'pcJ-2_2006': 0, 'pcJ-3': 1, 'pcJ-3_2006': 0, 'pcJ-4': 1, 'pcJ-4_2006': 0, 'pcS-0': 0, 'pcS-1': 0, 'pcS-2': 0, 'pcS-3': 0, 'pcS-4': 0, 'pcseg-0': 1, 'pcseg-1': 1, 'pcseg-2': 1, 'pcseg-3': 1, 'pcseg-4': 1, 'pcSseg-0': 1, 'pcSseg-1': 1, 'pcSseg-2': 1, 'pcSseg-3': 1, 'pcSseg-4': 1, 'pcX-1': 1, 'pcX-2': 1, 'pcX-3': 1, 'pcX-4': 1, 'pSBKJC': 0, 'Pt - mDZP': 0, 'pV6Z': 0, 'pV7Z': 0, 'Roos Augmented Double Zeta ANO': 0, 'Roos Augmented Triple Zeta ANO': 0, 's3-21G': 0, 's3-21G*': 0, 's6-31G': 0, 's6-31G*': 0, 'Sadlej pVTZ': 1, 'Sadlej+': 1, 'sap_grasp_large': 1, 'sap_grasp_small': 1, 'sap_helfem_large': 1, 'sap_helfem_small': 1, 'Sapporo-DKH3-DZP-2012-diffuse': 1, 'Sapporo-DKH3-DZP-2012': 1, 'Sapporo-DKH3-DZP-diffuse': 1, 'Sapporo-DKH3-DZP': 1, 'Sapporo-DKH3-QZP-2012-diffuse': 1, 'Sapporo-DKH3-QZP-2012': 1, 'Sapporo-DKH3-QZP-diffuse': 1, 'Sapporo-DKH3-QZP': 1, 'Sapporo-DKH3-TZP-2012-diffuse': 1, 'Sapporo-DKH3-TZP-2012': 1, 'Sapporo-DKH3-TZP-diffuse': 1, 'Sapporo-DKH3-TZP': 1, 'Sapporo-DZP-2012-diffuse': 1, 'Sapporo-DZP-2012': 1, 'Sapporo-DZP-diffuse': 1, 'Sapporo-DZP': 1, 'Sapporo-QZP-2012-diffuse': 1, 'Sapporo-QZP-2012': 1, 'Sapporo-QZP-diffuse': 1, 'Sapporo-QZP': 1, 'Sapporo-TZP-2012-diffuse': 1, 'Sapporo-TZP-2012': 1, 'Sapporo-TZP-diffuse': 1, 'Sapporo-TZP': 1, 'SARC-DKH2': 0, 'SARC-ZORA': 0, 'SARC2-QZV-DKH2-JKFIT': 0, 'SARC2-QZV-DKH2': 0, 'SARC2-QZV-ZORA-JKFIT': 0, 'SARC2-QZV-ZORA': 0, 'SARC2-QZVP-DKH2-JKFIT': 0, 'SARC2-QZVP-DKH2': 0, 'SARC2-QZVP-ZORA-JKFIT': 0, 'SARC2-QZVP-ZORA': 0, 'SBKJC Polarized (p,2d) - LFK': 0, 'SBKJC-ECP': 0, 'SBKJC-VDZ': 0, 'SBO4-DZ(d)-3G': 1, 'SBO4-DZ(d,p)-3G': 1, 'SBO4-SZ-3G': 1, 'Scaled MINI': 0, 'STO-2G': 1, 'STO-3G': 1, 'STO-3G*': 1, 'STO-4G': 1, 'STO-5G': 1, 'STO-6G': 1, 'Stuttgart RLC ECP': 0, 'Stuttgart RLC': 0, 'Stuttgart RSC 1997 ECP': 0, 'Stuttgart RSC 1997': 0, 'Stuttgart RSC ANO': 0, 'Stuttgart RSC Segmented + ECP': 0, 'SV (Dunning-Hay)': 0, 'SV + Double Rydberg (Dunning-Hay)': 0, 'SV + Rydberg (Dunning-Hay)': 0, 'SVP (Dunning-Hay)': 0, 'SVP + Diffuse (Dunning-Hay)': 0, 'SVP + Diffuse + Rydberg (Dunning-Hay)': 0, 'SVP + Rydberg (Dunning-Hay)': 0, 'TZ (Dunning-Hay)': 0, 'TZP-ZORA': 1, 'UGBS': 0, 'un-ccemd-ref': 0, 'un-pcemd-ref': 0, 'Wachters+f': 0, 'WTBS': 0, 'x2c-JFIT-universal': 1, 'x2c-JFIT': 1, 'x2c-QZVPall-2c-s': 1, 'x2c-QZVPall-2c': 1, 'x2c-QZVPall-s': 1, 'x2c-QZVPall': 1, 'x2c-QZVPPall-2c-s': 1, 'x2c-QZVPPall-2c': 1, 'x2c-QZVPPall-s': 1, 'x2c-QZVPPall': 1, 'x2c-SV(P)all-2c': 0, 'x2c-SV(P)all-s': 1, 'x2c-SV(P)all': 0, 'x2c-SVPall-2c': 0, 'x2c-SVPall-s': 1, 'x2c-SVPall': 0, 'x2c-TZVPall-2c': 0, 'x2c-TZVPall-s': 1, 'x2c-TZVPall': 0, 'x2c-TZVPPall-2c': 0, 'x2c-TZVPPall-s': 1, 'x2c-TZVPPall': 0}
BSE_VERSIONNUMBERS = {'sdd' : 0, '2zapa-nr-cv': 1, '2zapa-nr': 1, '3-21g': 1, '3zapa-nr-cv': 1, '3zapa-nr': 1, '4-31g': 1, '4zapa-nr-cv': 1, '4zapa-nr': 1, '5-21g': 1, '5zapa-nr-cv': 1, '5zapa-nr': 1, '6-21g': 1, '6-31++g': 1, '6-31++g*': 1, '6-31++g**-j': 0, '6-31++g**': 1, '6-31+g': 1, '6-31+g*-j': 0, '6-31+g*': 1, '6-31+g**': 1, '6-311++g(2d,2p)': 0, '6-311++g(3df,3pd)': 0, '6-311++g': 0, '6-311++g*': 0, '6-311++g**-j': 0, '6-311++g**': 0, '6-311+g(2d,p)': 0, '6-311+g': 0, '6-311+g*-j': 0, '6-311+g*': 0, '6-311+g**': 0, '6-311g(2df,2pd)': 0, '6-311g(d,p)': 0, '6-311g-j': 0, '6-311g': 0, '6-311g*': 0, '6-311g**-rifit': 1, '6-311g**': 0, '6-311xxg(d,p)': 1, '6-31g(2df,p)': 0, '6-31g(3df,3pd)': 0, '6-31g(d,p)': 1, '6-31g-blaudeau': 0, '6-31g-j': 0, '6-31g': 1, '6-31g*-blaudeau': 0, '6-31g*': 1, '6-31g**-rifit': 1, '6-31g**': 1, '6zapa-nr': 1, '7zapa-nr': 1, 'acv2z-j': 1, 'acv3z-j': 1, 'acv4z-j': 1, 'admm-1': 1, 'admm-2': 1, 'admm-3': 1, 'ahgbs-5': 1, 'ahgbs-7': 1, 'ahgbs-9': 1, 'ahgbsp1-5': 1, 'ahgbsp1-7': 1, 'ahgbsp1-9': 1, 'ahgbsp2-5': 1, 'ahgbsp2-7': 1, 'ahgbsp2-9': 1, 'ahgbsp3-5': 1, 'ahgbsp3-7': 1, 'ahgbsp3-9': 1, 'ahlrichs pvdz': 0, 'ahlrichs tzv': 0, 'ahlrichs vdz': 0, 'ahlrichs vtz': 0, 'ano-dk3': 1, 'ano-r': 2, 'ano-r0': 2, 'ano-r1': 2, 'ano-r2': 2, 'ano-r3': 2, 'ano-rcc-mb': 1, 'ano-rcc-vdz': 1, 'ano-rcc-vdzp': 1, 'ano-rcc-vqzp': 1, 'ano-rcc-vtz': 1, 'ano-rcc-vtzp': 1, 'ano-rcc': 1, 'ano-vt-dz': 1, 'ano-vt-qz': 2, 'ano-vt-tz': 1, 'apr-cc-pv(q+d)z': 0, 'atzp-zora': 1, 'aug-admm-1': 1, 'aug-admm-2': 1, 'aug-admm-3': 1, 'aug-cc-pcv5z': 0, 'aug-cc-pcvdz-dk': 0, 'aug-cc-pcvdz': 0, 'aug-cc-pcvqz-dk': 0, 'aug-cc-pcvqz': 0, 'aug-cc-pcvtz-dk': 0, 'aug-cc-pcvtz': 0, 'aug-cc-pv(5+d)z': 1, 'aug-cc-pv(d+d)z': 1, 'aug-cc-pv(q+d)z': 1, 'aug-cc-pv(t+d)z': 1, 'aug-cc-pv5z-dk': 0, 'aug-cc-pv5z-optri': 0, 'aug-cc-pv5z-pp-optri': 0, 'aug-cc-pv5z-pp-rifit': 0, 'aug-cc-pv5z-pp': 0, 'aug-cc-pv5z-rifit': 1, 'aug-cc-pv5z': 1, 'aug-cc-pv6z-rifit': 1, 'aug-cc-pv6z': 1, 'aug-cc-pv7z': 0, 'aug-cc-pvdz-dk': 0, 'aug-cc-pvdz-dk3': 1, 'aug-cc-pvdz-optri': 0, 'aug-cc-pvdz-pp-optri': 0, 'aug-cc-pvdz-pp-rifit': 0, 'aug-cc-pvdz-pp': 0, 'aug-cc-pvdz-rifit': 1, 'aug-cc-pvdz-x2c': 1, 'aug-cc-pvdz': 1, 'aug-cc-pvqz-dk': 0, 'aug-cc-pvqz-dk3': 1, 'aug-cc-pvqz-optri': 0, 'aug-cc-pvqz-pp-optri': 0, 'aug-cc-pvqz-pp-rifit': 0, 'aug-cc-pvqz-pp': 0, 'aug-cc-pvqz-rifit': 1, 'aug-cc-pvqz-x2c': 1, 'aug-cc-pvqz': 1, 'aug-cc-pvtz-dk': 0, 'aug-cc-pvtz-dk3': 1, 'aug-cc-pvtz-j': 0, 'aug-cc-pvtz-optri': 0, 'aug-cc-pvtz-pp-optri': 0, 'aug-cc-pvtz-pp-rifit': 0, 'aug-cc-pvtz-pp': 0, 'aug-cc-pvtz-rifit': 1, 'aug-cc-pvtz-x2c': 1, 'aug-cc-pvtz': 1, 'aug-cc-pwcv5z-dk': 0, 'aug-cc-pwcv5z-pp-optri': 0, 'aug-cc-pwcv5z-pp-rifit': 0, 'aug-cc-pwcv5z-pp': 0, 'aug-cc-pwcv5z-rifit': 1, 'aug-cc-pwcv5z': 0, 'aug-cc-pwcvdz-dk3': 1, 'aug-cc-pwcvdz-pp-optri': 0, 'aug-cc-pwcvdz-pp-rifit': 0, 'aug-cc-pwcvdz-pp': 0, 'aug-cc-pwcvdz-rifit': 1, 'aug-cc-pwcvdz-x2c': 1, 'aug-cc-pwcvdz': 0, 'aug-cc-pwcvqz-dk': 0, 'aug-cc-pwcvqz-dk3': 1, 'aug-cc-pwcvqz-pp-optri': 0, 'aug-cc-pwcvqz-pp-rifit': 0, 'aug-cc-pwcvqz-pp': 0, 'aug-cc-pwcvqz-rifit': 1, 'aug-cc-pwcvqz-x2c': 1, 'aug-cc-pwcvqz': 0, 'aug-cc-pwcvtz-dk': 0, 'aug-cc-pwcvtz-dk3': 1, 'aug-cc-pwcvtz-pp-optri': 0, 'aug-cc-pwcvtz-pp-rifit': 0, 'aug-cc-pwcvtz-pp': 0, 'aug-cc-pwcvtz-rifit': 1, 'aug-cc-pwcvtz-x2c': 1, 'aug-cc-pwcvtz': 0, 'aug-ccx-5z': 1, 'aug-ccx-dz': 1, 'aug-ccx-qz': 1, 'aug-ccx-tz': 1, 'aug-mcc-pv5z': 0, 'aug-mcc-pv6z': 0, 'aug-mcc-pv7z': 0, 'aug-mcc-pv8z': 0, 'aug-mcc-pvqz': 0, 'aug-mcc-pvtz': 0, 'aug-pc-0': 0, 'aug-pc-1': 0, 'aug-pc-2': 0, 'aug-pc-3': 0, 'aug-pc-4': 0, 'aug-pch-1': 1, 'aug-pch-2': 1, 'aug-pch-3': 1, 'aug-pch-4': 1, 'aug-pcj-0': 1, 'aug-pcj-0_2006': 0, 'aug-pcj-1': 1, 'aug-pcj-1_2006': 0, 'aug-pcj-2': 1, 'aug-pcj-2_2006': 0, 'aug-pcj-3': 1, 'aug-pcj-3_2006': 0, 'aug-pcj-4': 1, 'aug-pcj-4_2006': 0, 'aug-pcs-0': 0, 'aug-pcs-1': 0, 'aug-pcs-2': 0, 'aug-pcs-3': 0, 'aug-pcs-4': 0, 'aug-pcseg-0': 1, 'aug-pcseg-1': 1, 'aug-pcseg-2': 1, 'aug-pcseg-3': 1, 'aug-pcseg-4': 1, 'aug-pcsseg-0': 1, 'aug-pcsseg-1': 1, 'aug-pcsseg-2': 1, 'aug-pcsseg-3': 1, 'aug-pcsseg-4': 1, 'aug-pcx-1': 1, 'aug-pcx-2': 1, 'aug-pcx-3': 1, 'aug-pcx-4': 1, 'aug-pv7z': 0, 'binning 641(d)': 0, 'binning 641(df)': 0, 'binning 641+(d)': 0, 'binning 641+(df)': 0, 'binning 641+': 0, 'binning 641': 0, 'binning 962(d)': 0, 'binning 962(df)': 0, 'binning 962+(d)': 0, 'binning 962+(df)': 0, 'binning 962+': 0, 'binning 962': 0, 'cc-pcv5z': 0, 'cc-pcvdz-dk': 0, 'cc-pcvdz-f12-optri': 0, 'cc-pcvdz-f12-rifit': 0, 'cc-pcvdz-f12': 0, 'cc-pcvdz': 0, 'cc-pcvqz-dk': 0, 'cc-pcvqz-f12-optri': 0, 'cc-pcvqz-f12-rifit': 0, 'cc-pcvqz-f12': 0, 'cc-pcvqz': 0, 'cc-pcvtz-dk': 0, 'cc-pcvtz-f12-optri': 0, 'cc-pcvtz-f12-rifit': 0, 'cc-pcvtz-f12': 0, 'cc-pcvtz': 0, 'cc-pv(5+d)z': 1, 'cc-pv(d+d)z': 1, 'cc-pv(q+d)z': 1, 'cc-pv(t+d)z': 1, 'cc-pv5z(fi/sf/fw)': 0, 'cc-pv5z(fi/sf/lc)': 0, 'cc-pv5z(fi/sf/sc)': 0, 'cc-pv5z(pt/sf/fw)': 0, 'cc-pv5z(pt/sf/lc)': 0, 'cc-pv5z(pt/sf/sc)': 0, 'cc-pv5z-dk': 0, 'cc-pv5z-f12(rev2)': 1, 'cc-pv5z-f12': 1, 'cc-pv5z-jkfit': 1, 'cc-pv5z-pp-rifit': 0, 'cc-pv5z-pp': 0, 'cc-pv5z-rifit': 1, 'cc-pv5z': 1, 'cc-pv6z-rifit': 1, 'cc-pv6z': 1, 'cc-pv8z': 0, 'cc-pv9z': 0, 'cc-pvdz(fi/sf/fw)': 0, 'cc-pvdz(fi/sf/lc)': 0, 'cc-pvdz(fi/sf/sc)': 0, 'cc-pvdz(pt/sf/fw)': 0, 'cc-pvdz(pt/sf/lc)': 0, 'cc-pvdz(pt/sf/sc)': 0, 'cc-pvdz(seg-opt)': 0, 'cc-pvdz-dk': 0, 'cc-pvdz-dk3': 1, 'cc-pvdz-f12(rev2)': 1, 'cc-pvdz-f12-optri': 0, 'cc-pvdz-f12': 0, 'cc-pvdz-pp-rifit': 0, 'cc-pvdz-pp': 0, 'cc-pvdz-rifit': 1, 'cc-pvdz-x2c': 1, 'cc-pvdz': 1, 'cc-pvqz(fi/sf/fw)': 0, 'cc-pvqz(fi/sf/lc)': 0, 'cc-pvqz(fi/sf/sc)': 0, 'cc-pvqz(pt/sf/fw)': 0, 'cc-pvqz(pt/sf/lc)': 0, 'cc-pvqz(pt/sf/sc)': 0, 'cc-pvqz(seg-opt)': 0, 'cc-pvqz-dk': 0, 'cc-pvqz-dk3': 1, 'cc-pvqz-f12(rev2)': 1, 'cc-pvqz-f12-optri': 0, 'cc-pvqz-f12': 0, 'cc-pvqz-jkfit': 1, 'cc-pvqz-pp-rifit': 0, 'cc-pvqz-pp': 0, 'cc-pvqz-rifit': 1, 'cc-pvqz-x2c': 1, 'cc-pvqz': 1, 'cc-pvtz(fi/sf/fw)': 0, 'cc-pvtz(fi/sf/lc)': 0, 'cc-pvtz(fi/sf/sc)': 0, 'cc-pvtz(pt/sf/fw)': 0, 'cc-pvtz(pt/sf/lc)': 0, 'cc-pvtz(pt/sf/sc)': 0, 'cc-pvtz(seg-opt)': 0, 'cc-pvtz-dk': 0, 'cc-pvtz-dk3': 1, 'cc-pvtz-f12(rev2)': 1, 'cc-pvtz-f12-optri': 0, 'cc-pvtz-f12': 0, 'cc-pvtz-jkfit': 1, 'cc-pvtz-pp-rifit': 0, 'cc-pvtz-pp': 0, 'cc-pvtz-rifit': 1, 'cc-pvtz-x2c': 1, 'cc-pvtz': 1, 'cc-pwcv5z-dk': 0, 'cc-pwcv5z-pp-rifit': 0, 'cc-pwcv5z-pp': 0, 'cc-pwcv5z-rifit': 1, 'cc-pwcv5z': 0, 'cc-pwcvdz-dk3': 1, 'cc-pwcvdz-pp-rifit': 0, 'cc-pwcvdz-pp': 0, 'cc-pwcvdz-rifit': 1, 'cc-pwcvdz-x2c': 1, 'cc-pwcvdz': 0, 'cc-pwcvqz-dk': 0, 'cc-pwcvqz-dk3': 2, 'cc-pwcvqz-pp-rifit': 0, 'cc-pwcvqz-pp': 0, 'cc-pwcvqz-rifit': 1, 'cc-pwcvqz-x2c': 1, 'cc-pwcvqz': 0, 'cc-pwcvtz-dk': 0, 'cc-pwcvtz-dk3': 1, 'cc-pwcvtz-pp-rifit': 0, 'cc-pwcvtz-pp': 0, 'cc-pwcvtz-rifit': 1, 'cc-pwcvtz-x2c': 1, 'cc-pwcvtz': 0, 'ccemd-2': 0, 'ccemd-3': 0, 'ccj-pv5z': 0, 'ccj-pvdz': 0, 'ccj-pvqz': 0, 'ccj-pvtz': 0, 'ccx-5z': 1, 'ccx-dz': 1, 'ccx-qz': 1, 'ccx-tz': 1, 'coemd-2': 0, 'coemd-3': 0, 'coemd-4': 0, 'coemd-ref': 0, 'cologne dkh2': 0, 'crenbl ecp': 0, 'crenbl': 0, 'crenbs ecp': 0, 'crenbs': 0, 'd-aug-cc-pv5z': 0, 'd-aug-cc-pv6z': 0, 'd-aug-cc-pvdz': 0, 'd-aug-cc-pvqz': 0, 'd-aug-cc-pvtz': 0, 'def2-ecp': 1, 'def2-qzvp-rifit': 1, 'def2-qzvp': 1, 'def2-qzvpd': 1, 'def2-qzvpp-rifit': 1, 'def2-qzvpp': 1, 'def2-qzvppd-rifit': 1, 'def2-qzvppd': 1, 'def2-sv(p)-jkfit': 1, 'def2-sv(p)-rifit': 1, 'def2-sv(p)': 1, 'def2-svp-rifit': 1, 'def2-svp': 1, 'def2-svpd-rifit': 1, 'def2-svpd': 1, 'def2-tzvp-rifit': 1, 'def2-tzvp': 1, 'def2-tzvpd-rifit': 1, 'def2-tzvpd': 1, 'def2-tzvpp-rifit': 1, 'def2-tzvpp': 1, 'def2-tzvppd-rifit': 1, 'def2-tzvppd': 1, 'def2-universal-jfit': 1, 'def2-universal-jkfit': 1, 'demon2k-dzvp-gga': 1, 'dfo+-nrlmol': 1, 'dfo-1-bhs': 1, 'dfo-1': 1, 'dfo-2': 1, 'dfo-nrlmol': 1, 'dgauss-a1-dftjfit': 0, 'dgauss-a1-dftxfit': 0, 'dgauss-a2-dftjfit': 0, 'dgauss-a2-dftxfit': 0, 'dgauss-dzvp': 0, 'dgauss-dzvp2': 0, 'dgauss-tzvp': 0, 'dhf-ecp': 0, 'dhf-qzvp': 0, 'dhf-qzvpp': 0, 'dhf-sv(p)': 0, 'dhf-svp': 0, 'dhf-tzvp': 0, 'dhf-tzvpp': 0, 'dz (dunning-hay)': 0, 'dz + double rydberg (dunning-hay)': 0, 'dz + rydberg (dunning-hay)': 0, 'dzp (dunning-hay)': 0, 'dzp + diffuse (dunning-hay)': 0, 'dzp + rydberg (dunning-hay)': 0, 'fano-5z': 1, 'fano-6z': 1, 'fano-dz': 1, 'fano-qz': 1, 'fano-tz': 1, 'hgbs-5': 1, 'hgbs-7': 1, 'hgbs-9': 1, 'hgbsp1-5': 1, 'hgbsp1-7': 1, 'hgbsp1-9': 1, 'hgbsp2-5': 1, 'hgbsp2-7': 1, 'hgbsp2-9': 1, 'hgbsp3-5': 1, 'hgbsp3-7': 1, 'hgbsp3-9': 1, 'iglo-ii': 0, 'iglo-iii': 0, 'jgauss-dzp': 1, 'jgauss-qz2p': 1, 'jgauss-qzp': 1, 'jgauss-tzp1': 1, 'jgauss-tzp2': 1, 'jorge-5zp-dkh': 1, 'jorge-5zp': 1, 'jorge-6zp-dkh': 1, 'jorge-6zp': 1, 'jorge-a5zp': 1, 'jorge-adzp': 1, 'jorge-aqzp': 1, 'jorge-atzp': 1, 'jorge-dzp-dkh': 1, 'jorge-dzp': 1, 'jorge-qzp-dkh': 1, 'jorge-qzp': 1, 'jorge-tzp-dkh': 1, 'jorge-tzp': 1, 'jul-cc-pv(d+d)z': 0, 'jul-cc-pv(q+d)z': 0, 'jul-cc-pv(t+d)z': 0, 'jun-cc-pv(d+d)z': 0, 'jun-cc-pv(q+d)z': 0, 'jun-cc-pv(t+d)z': 0, 'koga unpolarized': 1, 'lanl08(d)': 0, 'lanl08(f)': 0, 'lanl08+': 0, 'lanl08': 0, 'lanl2dz ecp': 0, 'lanl2dz': 0, 'lanl2dzdp': 0, 'lanl2tz(f)': 0, 'lanl2tz+': 0, 'lanl2tz': 0, 'm6-31g': 0, 'm6-31g*': 0, 'maug-cc-pv(d+d)z': 0, 'maug-cc-pv(q+d)z': 0, 'maug-cc-pv(t+d)z': 0, 'may-cc-pv(q+d)z': 0, 'may-cc-pv(t+d)z': 0, 'midi!': 1, 'midi': 0, 'midix': 1, 'mini': 0, 'modified-lanl2dz': 0, 'nasa ames ano': 0, 'nasa ames ano2': 0, 'nasa ames cc-pcv5z': 0, 'nasa ames cc-pcvqz': 0, 'nasa ames cc-pcvtz': 0, 'nasa ames cc-pv5z': 0, 'nasa ames cc-pvqz': 0, 'nasa ames cc-pvtz': 0, 'nlo-v': 0, 'nmr-dkh (tz2p)': 0, 'orp': 1, 'partridge uncontracted 1': 0, 'partridge uncontracted 2': 0, 'partridge uncontracted 3': 0, 'partridge uncontracted 4': 0, 'pc-0': 0, 'pc-1': 0, 'pc-2': 0, 'pc-3': 0, 'pc-4': 0, 'pcemd-2': 0, 'pcemd-3': 0, 'pcemd-4': 0, 'pch-1': 1, 'pch-2': 1, 'pch-3': 1, 'pch-4': 1, 'pcj-0': 1, 'pcj-0_2006': 0, 'pcj-1': 1, 'pcj-1_2006': 0, 'pcj-2': 1, 'pcj-2_2006': 0, 'pcj-3': 1, 'pcj-3_2006': 0, 'pcj-4': 1, 'pcj-4_2006': 0, 'pcs-0': 0, 'pcs-1': 0, 'pcs-2': 0, 'pcs-3': 0, 'pcs-4': 0, 'pcseg-0': 1, 'pcseg-1': 1, 'pcseg-2': 1, 'pcseg-3': 1, 'pcseg-4': 1, 'pcsseg-0': 1, 'pcsseg-1': 1, 'pcsseg-2': 1, 'pcsseg-3': 1, 'pcsseg-4': 1, 'pcx-1': 1, 'pcx-2': 1, 'pcx-3': 1, 'pcx-4': 1, 'psbkjc': 0, 'pt - mdzp': 0, 'pv6z': 0, 'pv7z': 0, 'roos augmented double zeta ano': 0, 'roos augmented triple zeta ano': 0, 's3-21g': 0, 's3-21g*': 0, 's6-31g': 0, 's6-31g*': 0, 'sadlej pvtz': 1, 'sadlej+': 1, 'sap_grasp_large': 1, 'sap_grasp_small': 1, 'sap_helfem_large': 1, 'sap_helfem_small': 1, 'sapporo-dkh3-dzp-2012-diffuse': 1, 'sapporo-dkh3-dzp-2012': 1, 'sapporo-dkh3-dzp-diffuse': 1, 'sapporo-dkh3-dzp': 1, 'sapporo-dkh3-qzp-2012-diffuse': 1, 'sapporo-dkh3-qzp-2012': 1, 'sapporo-dkh3-qzp-diffuse': 1, 'sapporo-dkh3-qzp': 1, 'sapporo-dkh3-tzp-2012-diffuse': 1, 'sapporo-dkh3-tzp-2012': 1, 'sapporo-dkh3-tzp-diffuse': 1, 'sapporo-dkh3-tzp': 1, 'sapporo-dzp-2012-diffuse': 1, 'sapporo-dzp-2012': 1, 'sapporo-dzp-diffuse': 1, 'sapporo-dzp': 1, 'sapporo-qzp-2012-diffuse': 1, 'sapporo-qzp-2012': 1, 'sapporo-qzp-diffuse': 1, 'sapporo-qzp': 1, 'sapporo-tzp-2012-diffuse': 1, 'sapporo-tzp-2012': 1, 'sapporo-tzp-diffuse': 1, 'sapporo-tzp': 1, 'sarc-dkh2': 0, 'sarc-zora': 0, 'sarc2-qzv-dkh2-jkfit': 0, 'sarc2-qzv-dkh2': 0, 'sarc2-qzv-zora-jkfit': 0, 'sarc2-qzv-zora': 0, 'sarc2-qzvp-dkh2-jkfit': 0, 'sarc2-qzvp-dkh2': 0, 'sarc2-qzvp-zora-jkfit': 0, 'sarc2-qzvp-zora': 0, 'sbkjc polarized (p,2d) - lfk': 0, 'sbkjc-ecp': 0, 'sbkjc-vdz': 0, 'sbo4-dz(d)-3g': 1, 'sbo4-dz(d,p)-3g': 1, 'sbo4-sz-3g': 1, 'scaled mini': 0, 'sto-2g': 1, 'sto-3g': 1, 'sto-3g*': 1, 'sto-4g': 1, 'sto-5g': 1, 'sto-6g': 1, 'stuttgart rlc ecp': 0, 'stuttgart rlc': 0, 'stuttgart rsc 1997 ecp': 0, 'stuttgart rsc 1997': 0, 'stuttgart rsc ano': 0, 'stuttgart rsc segmented + ecp': 0, 'sv (dunning-hay)': 0, 'sv + double rydberg (dunning-hay)': 0, 'sv + rydberg (dunning-hay)': 0, 'svp (dunning-hay)': 0, 'svp + diffuse (dunning-hay)': 0, 'svp + diffuse + rydberg (dunning-hay)': 0, 'svp + rydberg (dunning-hay)': 0, 'tz (dunning-hay)': 0, 'tzp-zora': 1, 'ugbs': 0, 'un-ccemd-ref': 0, 'un-pcemd-ref': 0, 'wachters+f': 0, 'wtbs': 0, 'x2c-jfit-universal': 1, 'x2c-jfit': 1, 'x2c-qzvpall-2c-s': 1, 'x2c-qzvpall-2c': 1, 'x2c-qzvpall-s': 1, 'x2c-qzvpall': 1, 'x2c-qzvppall-2c-s': 1, 'x2c-qzvppall-2c': 1, 'x2c-qzvppall-s': 1, 'x2c-qzvppall': 1, 'x2c-sv(p)all-2c': 0, 'x2c-sv(p)all-s': 1, 'x2c-sv(p)all': 0, 'x2c-svpall-2c': 0, 'x2c-svpall-s': 1, 'x2c-svpall': 0, 'x2c-tzvpall-2c': 0, 'x2c-tzvpall-s': 1, 'x2c-tzvpall': 0, 'x2c-tzvppall-2c': 0, 'x2c-tzvppall-s': 1, 'x2c-tzvppall': 0}

# Constant containing all the possible allowed versions of 'yes' the user may input
YES = ['y', 'yes']


##
# COMPLETE TEST FOR MODIFIER.PY 
def test () :
    fileList = ['1_N1_CF3_H_perp.log']
    #fileList=['$RECYCLE.BIN', '1_N1_CF3_H_perp.log', '1_N1_CF3_H_perp_pcm.log', '1_N1_CF3_H_planar.log', '1_N1_CF3_H_planar_pcm.log', '1_N1_CH3_H_perp.log', '1_N1_CH3_H_perp_pcm.log', '1_N1_CH3_H_planar.log', '1_N1_CH3_H_planar_pcm.log', '1_N1_H_H_perp_pcm.log', '1_N1_H_H_planar_pcm.log', '1_N1_PNO2_H_perp.log', '1_N1_PNO2_H_perp_pcm.log', '1_N1_PNO2_H_planar.log', '1_N1_PNO2_H_planar_pcm.log', '1_N1_POMe_H_perp.log', '1_N1_POMe_H_perp_pcm.log', '1_N1_POMe_H_planar.log', '1_N1_POMe_H_planar_pcm.log', '2_N1_CF3_H_perp_pcm.log', '2_N1_CF3_H_planar_pcm.log', '2_N1_CH3_H_perp_pcm.log', '2_N1_CH3_H_planar_pcm.log', '2_N1_H_H_perp_pcm 2.log', '2_N1_H_H_perp_pcm.log', '2_N1_H_H_planar_pcm 2.log', '2_N1_H_H_planar_pcm.log', '2_N1_PNO2_H_perp_pcm 2.log', '2_N1_PNO2_H_perp_pcm.log', '2_N1_PNO2_H_planar_pcm 2.log', '2_N1_PNO2_H_planar_pcm.log', '2_N1_POMe_H_perp_pcm 2.log', '2_N1_POMe_H_perp_pcm.log', '2_N1_POMe_H_planar_pcm 2.log', '2_N1_POMe_H_planar_pcm.log', '3_N1_CF3_H_perp_pcm 2.log', '3_N1_CF3_H_perp_pcm.log', '3_N1_CF3_H_planar_pcm 2.log', '3_N1_CF3_H_planar_pcm.log', '3_N1_CH3_H_perp_pcm 2.log', '3_N1_CH3_H_perp_pcm.log', '3_N1_CH3_H_planar_pcm 2.log', '3_N1_CH3_H_planar_pcm.log', '3_N1_H_H_perp_pcm 2.log', '3_N1_H_H_perp_pcm.log', '3_N1_H_H_planar_pcm 2.log', '3_N1_H_H_planar_pcm.log', '3_N1_PNO2_H_perp_pcm.log', '3_N1_PNO2_H_planar_pcm 2.log', '3_N1_PNO2_H_planar_pcm.log', '3_N1_POMe_H_perp_pcm 2.log', '3_N1_POMe_H_perp_pcm.log', '3_N1_POMe_H_planar_pcm 2.log', '3_N1_POMe_H_planar_pcm.log', 'Biphenyl_excited 2.log', 'Biphenyl_excited.log', 'C1 2.log', 'C1.log', 'C2 2.log', 'C2.log', 'GoodVibes-3.0.1', 'N1 2.log', 'N1.log', 'N2 2.log', 'N2.log', 'N3 2.log', 'N3.log', 'N4 2.log', 'N4.log', 'P1 2.log', 'P1.log', 'P2 2.log', 'P2.log', 'P3 2.log', 'P3.log', 'P4 2.log', 'P4.log', 'P_0_CF3_H_pcm 2.log', 'P_0_CF3_H_pcm.log', 'P_0_CH3_H_pcm 2.log', 'P_0_CH3_H_pcm.log', 'P_0_H_H_pcm.log', 'P_0_PNO2_H_pcm 2.log', 'P_0_PNO2_H_pcm.log', 'P_0_POMe_H_pcm 2.log', 'P_0_POMe_H_pcm.log', 'R_0_CF3_H 2.log', 'R_0_CF3_H.log', 'R_0_CH3_H 2.log', 'R_0_CH3_H.log', 'R_0_H_H 2.log', 'R_0_H_H.log', 'R_0_PNO2_H 2.log', 'R_0_PNO2_H.log', 'R_0_POMe_H 2.log', 'R_0_POMe_H.log', 'R_N1_0_0.log', 'Z_Br_PH3_Br_P-SP 2.log', 'Z_Br_PH3_Br_P-SP.gjf', 'Z_Br_PH3_Br_P-SP.log', 'Z_Br_PH3_Br_P.gjf', 'Z_Br_PH3_Br_P.log', 'modifier_v03.py', 'scratch2.py']
    header = "%nprocshared=60\n%mem=60GB\n%chk\n# b2plypd3 gen pseudo=read nosymm scrf=(read,pcm,solvent=chloroform)\n\n"
    header = removeConnectivity(header)
    basisSetName, primaryKey = get_basisSetName()          # Try primary with '6-31G', secondary as 'lanl2dz' for Au (Gold)
    #basisSetName = {"6-31g" : ["Primary"], "lanl2dz" : ["79"]}
    #primaryKey = "6-31g"
    footer = "\n"
    newExtension = "yes"
    if newExtension in YES :
        file_ext = "-SP"
    else :
        file_ext = ''
    outfileDict = {}
    notEdited = list()
    for file in fileList :
        outContents = prepOutfile(file,basisSetName,primaryKey,header,footer)
        if outContents == None :
            notEdited.append(file)
            fileList.remove(file)
        else :
            outfileDict[file] = outContents
    saveView(fileList,file_ext,outfileDict)
    if len(notEdited) > 0 :
        print("-"*50)
        print("The following file(s) were not edited:")
        for file in notEdited :
            print(file)
        print("-"*50)

try :
    main()
    #test()
except KeyboardInterrupt :
    print("\nmodifier_v03.py terminated.")

# NOTES FOR LATER
#    Maybe there is an option to do advanced inputs, this will cover charge/multiplicity
#    chargeInput = str(input("Do all of the files have the same charge or multiplicity?")
