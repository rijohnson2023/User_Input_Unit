# Goal

> The purpose of this unit is to collect user input from the command line and format it into a header or footer object

**Note:** More information about the objects created in this class can be found in the User_Input_Class document attached to this card.

## Key Features

> Inputs are by default collected by typing in an integer corresponding to the option displaying the correct input

> The final option for each section is *Other*, which prompts the user to type in their desired input for the header or footer object

> The user first constructs the header object, then is asked if they would like to create a footer object.

## Key Take-Aways

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

## Syntax Rules with the Gaussian Input Files

- Input is free format and case-insensitive

- Spaces, tabs, commas, or forward slashes can be used in any combination to separate items within a line. Multiple spaces are treated like a single delimitator

- Options to keywords may be specified in any of the following forms

    - Keyword=option
    - Keyword(option)
    - Keyword=(option1,option2,option…)
    - Keyword(option1,option2,option…)

- Multiple options are enclosed in parenthesis and separated by any valid delimitator (though commas are conventional).

- The equals sign before the opening parenthesis may be omitted, or spaces may optionally be included before or after the equals sign.

- All keywords may be shortened to their shortest unique abbreviation within the entire Gaussian 16 system.

- The contents of an external file may be included within the G16 input file using the following syntax: ‘@filename’. This causes the entire file to be placed at the current location in the input stream.

- Comments begin with an exclamation point (!), which may appear anywhere on a line. Separate comment lines may appear anywhere within the input file.

# Big Brain Stuff

## Classification

> This unit could be a class
> Only most of the inputs are characteristic of the header and footer across all files
> Each file though is an instance.
>> There could be Route Section keywords that are specific to the molecule, or the atoms in the molecule
>> These keywords need to be addressed separately
>>> The Route Section keywords that will vary based on the molecule or atoms in the molecule are the Basis Set and Additional Route Section Inputs

> So all of the ui can be saved as class variables, but upon constructing the header, only the right variables needed for the instance are accessed.
> Therefore, there should be two other classes for the header object and the footer object, and these classes are dependent on both the ui and the file input (fi)

> So the outputs from this unit can be the lists of keywords for each section, strings representing each line, or the objects themselves with additional inputs, i.e. basis set instructions

## Theory for best user experience

> What knowledge needs to be known before the user gives the inputs?
> The question is what knowledge is required for the user to complete the task
> So, the task should determine what information is fed to them
> Now, any data can be created, but we only want to give the user information when they need it
> And we don't just want to give them information, but we want to give them whatever they need so that
any decision the user needs to make is not made with uncertainty. We want them to make *calculation setup decisions* with perfect information

> So, we must think of what could be an uncertainty when the user is putting in input
> The only potential uncertainty is the contents of the file, the user may not be able to remember all of the atoms in all of the files they are operating on when editing files at scale. I.e. >= 100 files

# PseudoCode for the program

## Link0 Section
    print(Please choose all link0 inputs)
    print(most popular entries) # First entry is no additional input, two column, 10 objects total
    uiList = list()
    while input != 1 :
        ui = input() # Input cannot be 0, and must be in range
        if ui in uiData :
            uiList.append(ui)
        else:
            # Ask again
    link0Section = "\n".join(uiList)

## Route Section *#*
    print(The following questions will construct the Route section for the input files)
    print(When answering this section, consider all keywords that should be applied to all files specified.)
    print(Keywords that are specific to a file, molecule, or atom type will be specified later.)

### Job Type
    print(Set job type)
    print(Most Popular Jobs)
    ui_jt = input()

### Job Method
    print(Set method)
    print(Most Popular Job Methods)
    ui_jm = input()

### Basis Set
    print(The atoms in the file being edited include)
    print(Set a single basis set or set multiple basis sets)
    if input == 1 : # 1 is single, 2 is multiple
        print(Set Basis Set)
        print(Most popular basis sets)
        ui_bs_name = input()
    else:
        print(Setting up multiple basis sets specifies a primary basis set then all exceptions.)
        print(please specify the primary basis set)
        print(Most popular basis sets)
        ui_bs_primary = input
        while ui_bs_add_name != Enter or ui_bs_add_name != q : # Could also still use a menu here
            print(please specify an additional basis set)
            print(Most popular basis sets)
            ui_bs_add_name = inputs
            print(please specify the atoms under this set)
            print(Most popular basis atoms for this basis name)
            ui_bs_add_atoms = input

            if ui_bs_add_name != 1 : # option 1 is terminate sequence
                if ui_bs_add_name in bs_name_data : # Check to see if the basis name is valid if other
                    # Basis name is considered valid, now need to check all atoms for the specification
                    for atom in ui_bs_add_atoms :
                        if atom not in *Periodic Table* :
                            print(the atom is not in the periodic table, please specify atom again.)
                            atom = input()
                            while atom not in *Periodic Table* :
                                print(the atom is not in the periodic table, please specify atom again.)
                                atom = input()
                            ui_bs_add_atoms.replace(oldAtom, NewAtom)
                        else:
                            pass
                else:
                    print(input invalid)
                    print(Please specify another basis name)
                    print(most popular basis names)
                    ui_bs_add_name = input()
                    restart loop
            else:
                break

**Note** the best this section can do is create a partial order, because not all atoms will be specified. This section will require input
From the *File Input Unit*

### Solvent Model
    print(Set Solvent Model)
    print(Most Popular Solvent Models)
    ui_jm = input()

### Additional Route Section Inputs
    print(The atoms in the file being edited include)
    print(Set Additional Route Section Keywords)
    print(most popular entries) # First entry is no additional input, two column, 10 objects total
    uiList = list()
    while input != 1 :
        ui = input() # Input cannot be 0, and must be in range
        if ui in uiData :
            uiList.append(ui)
        else:
            # Ask again
    link0Section = "\n".join(uiList)

## Header and Footer reviews header and footer and saved objects
**Note:** Asks user if they would like to save the header and footer to a nickname. For example, this nickname can represent the type of experiment being conducted or the molecules being specified.

## Markdown Tutorial 

1. Open the file containing the Linux mascot.
2. Marvel at its beauty.

    ![Tux, the Linux mascot](/assets/images/tux.png)

3. Close the file.



