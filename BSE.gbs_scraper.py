import os
import pprint as pp

from Apps import PeriodicTable as PT

# Locate current working directory as destination for report
cwd_path = os.getcwd()
if not os.path.isdir(cwd_path + "/Data") :
    os.mkdir(cwd_path + "/Data")

dest_path = cwd_path + "/Data"

# Locate the periodic table module


# Directory with all of the .gbs files in it
dir_name = '/Users/Riley/Documents/Research/Scraping/basis_set_bundle-gaussian94-bib' 

# Create list of all the files in a the directory 
listoffiles = list()
for (dirpath, dir_names, filenames) in os.walk(dir_name):
    listoffiles += [os.path.join(dirpath,file) for file in filenames if file.split(".")[len(file.split("."))-1] == "gbs"]

print("Length of list of files: %d" % len(listoffiles))

with open(dest_path + "/gbs_scraper_data.py", "w") as record :
    # print the initial line to record all data
    record.write("basis_set_exchange_data = {")

    # iterate over all of the files in the directory with .gbs tail
    for file_path in listoffiles :
        # Splits on the / character and grabs last element
        file_name = file_path.split('/')[len(file_path.split('/'))-1]

        # Splits the file_name on the . character and grabs the first element (The basis name)
        basis_name = file_name.split(".")[0]
        version_number = int(file_name.split(".")[1])

        atom_list = list()

        # identifies atoms with basis functions under basis name
        with open(file_path,"r") as file :
            # Grab contents as a string
            contents = file.read()

        # Break down contents to the basis set objects for each atom
        complete_basis_object = contents.split("\n\n")[1]
        basis_objects_by_atom = complete_basis_object.split("****")

        # Collect the atom symbol
        for object in basis_objects_by_atom :
            lines = object.split("\n")
            try :
                line1 = lines[1].split()
                atom_symbol = line1[0]
                atom_list.append(atom_symbol)
            except IndexError:
                continue

        # Convert all atom symbols to atomic numbers 
        atomic_numbers = {PT.getNumber(atom) for atom in atom_list}

        # Create the line to be written into the record
        data = (version_number, atomic_numbers)
        line = ':'.join(["".join(["'",basis_name,"'"]),str(data)])

        # Write the line
        record.write("\n%s," % line)

        # Notify operator
        print("Completed: %s" % basis_name)

    # Print the final line in the record
    record.write("\n}")