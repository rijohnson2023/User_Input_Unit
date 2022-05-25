## Key Take-Aways from PseudoCode1:

***So, there are really three types of formats for how input is collected from the user***

> Option setup for single inputs
- Job Type (Same for all atoms)
- Job Method (Same for all atoms)
- Single Basis Set Model (Not always same for all atoms)
- Solvent Model (Same for all atoms)

> Option Setup for Multiples inputs
- Link0 Keywords (Same for all atoms)
- Additional Route Section Inputs (Not always same for all atoms)
> Basis Set Option Setup for Multiple Basis Sets (Not same for all atoms)

***User Inputs that might require information about the atoms in all of the calculation files are related to the basis set object and the additional route section keywords***

# PseudoCode for the program

## Link0 Section
    print(Please choose all link0 inputs)

    Menu1: # Please select a %s
        1. No additional %s inputs 
        2. First most popular
        3. Second most popular
        4. Third most popular
        5. Other

    UI_Link0_Section = input(list:str)

## Route Section *#*
    print(The following questions will construct the Route Section for the input files)
    print(When answering this section, consider all keywords that should be applied to all files specified.)
    print(Keywords that are specific to a file, molecule, or atom type will be specified later.)

### Job Type
    print(Set Job Type)

    Menu2: # Please select a %s
        1. Most Popular 
        2. Second most popular
        3. Third most popular
        4. Other

    UI_Job_Type = input(str:)

### Job Method
    print(Set Job Method)

    Menu2: # Please select a %s
        1. Most Popular 
        2. Second most popular
        3. Third most popular
        4. Other

    UI_Job_Method = input(str:)

### Basis Set Input

    print(Analyzing files)
    Create a set of all the atoms in the batch
    print(These files contain this set of atoms) # Requires special formatting

    Menu3:
        1. Apply single basis set to all atoms in the files
        2. Apply basis set to each atom
        3. Apply basis sets to subsets of atoms

    Menu3Input = input(str:)

    if Menu3Input == 1 :

        Menu2: # Please select a %s
            1. Most Popular 
            2. Second most popular
            3. Third most popular
            4. Other

        UI_Basis_Set_Name = input(str:)

    elif Menu3Input == 2 :
        for atom in "set of atoms" :
            print(Please select a basis set for this atom: %s) % atom

            Menu2: # Please select a %s
                1. Most Popular 
                2. Second most popular
                3. Third most popular
                4. Other

            UI_Basis_Set_Name = input(str:)

        # Add UI for Basis Set to dictionary
            if basisName in dict.keys():
                dict[basisName].add(atom)
            else:
                dict[basisName] = set(atom)

    else:
        print(These files contain this set of atoms: %s ) % batchSet.__repr__()

        batchSet = set of all atoms in the files
        loopCount: 1

        while batchSet is not empty:

            print(Please specify the %s subset of atoms: ) % loopCount.numberToText() # loop count 1 goes to 1st
            subset = input(set:str) # Case insensitive, deliminate by whitespace

            Menu2: # Please select a basis set name
                1. Most Popular Basis Set
                2. Second most popular
                3. Third most popular
                4. Other

            UI_Basis_Set_Name = input(str:)

            # Add UI for Basis Set to dictionary
            if basisname in dict():
                dict[basisName].add(set of atoms)
            else:
                dict[basisName] = (set of atoms)
            
            # eliminate subset from main set
            batchSet.eliminate(subset)

            loopCount += 1

**Output1:** {"basisName": {set of atoms}} # the atoms will be symbols, will need to convert

**Output2:** {"basisName1": {set of atoms 1},"basisName2": {set of atoms 2}, ...} # the atoms will be symbols, will need to convert

**Output3:** Same as output 2, the way its written will ensure no repeats

### Solvent Model
    print(Set Solvent Model)

    Menu1: # Please select a %s
        1. Most Popular 
        2. Second most popular
        3. Third most popular
        4. Other

    UI_Solvent_Model = input(str:)

### Additional Route Section Inputs
    print(The atoms in the file being edited include)
    print(Set Additional Route Section Keywords)

    Menu1: # Please select a %s
        1. No additional %s inputs 
        2. First most popular
        3. Second most popular
        4. Third most popular
        5. Other

    UI_ADD_Route_Section = input(list:)

# Unit Output
    Link0_Lines_BASE = "\n".join(UI_Link0_Section) 
    Route_Line_BASE = " ".join(UI_Job_Type,UI_Job_Method,UI_Solvent_Model,UI_ADD_Route_Section)
    Basis Basis Set Information

### Basis Set if pulling from BSE

**Output1:** {"basisName": {set of atoms}} # the atoms will be symbols, will need to convert

**Output2:** {"basisName1": {set of atoms 1},"basisName2": {set of atoms 2}, ...} # the atoms will be symbols, will need to convert

# Key take-Aways from PseudoCode2:

## Technical knowledge required

1. Ability to construct menus
- Menu 1
- Menu 2
- Menu 3
2. Ability to construct and edit dictionaries
3. Ability to work with sets
- eliminate subset from set
 - ability to add set to set

## Might be helpful to look up
1. Join string function, i.e. can I just pass strings and lists to the join function?

## Unsolved problems
1. What to do about keywords specific to files, molecules, sets of atoms, or atoms
2. Frozen Bond Angle, Bond length, or any modredundant information is still not collected at this point
   - This might be a problem for the fileInput class
   - This might involve some work related to keywords specific to files, molecules, sets of atoms, or atoms
3. What to do about basis set information that is going to go in the route section, not construct an object