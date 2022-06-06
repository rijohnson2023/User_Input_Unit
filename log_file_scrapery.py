import os, sys
import json, csv
from asyncore import file_wrapper

def set_data_path() -> str:
    outfile_name = input("\nName the file to store the data:\n(Do not include the extension)\n")

    # Locate current working directory as destination for report
    data_path = os.path.join(os.getcwd(),outfile_name)

    while True :
        # Two answers: acceptable: 1. path, 2. "", all else are bad"
        answer = str(input("\nThe data recorded will be at path:\n    %s\nHit enter to proceed, or type new path without '%s':\n  " % (data_path,outfile_name)))
        if answer == "" :
            break
        elif os.path.isdir(answer) :
            data_path = os.path.join(answer,outfile_name)
            break

    return data_path


def find_files_in_dir() -> list[str] :
    # Get valid source directory from user
    source_dir = input("\nPlease input the directory path to search:\n")
    while not os.path.isdir(source_dir) :
        source_dir = input("\nInvalid path, enter a new directory path to search:\n")

    # Create a list of all the log files in the directory
    listoffiles = list()
    for (dirpath, dir_names, filenames) in os.walk(source_dir):
        listoffiles += [os.path.join(dirpath,file) for file in filenames if file.split(".")[len(file.split("."))-1] == "log"]

    print("\n%d log files were found in the directory branch:\n%s" % (len(listoffiles), source_dir))
    return listoffiles


def check_log_file(file_path: str, file_obj: file_wrapper) -> bool :
    """
    Check log file searches the file object for the line
    "Normal termination of Gaussian 16"

    This is usually a substring of the last line in the log file, if it terminates correctly.
    Sometimes with multistep calculations, there will be a "Normal termination of Gaussian 16"
    line for every calculation step, or some may contain a "Error termination of Gaussian 16."

    We only want to record the keywords from the files that have terminated normally.
    Those keywords are deemed as valid by the Gaussian 16 software.
    Therefore, the log file must pass this check if we are going to count its keywords.

    This function iterates over the bytes/characters of the file in reverse order until it finds the line
    "Normal termination of Gaussian 16." Keep in mind that if the file contains multi-step calculations,
    and one of those calculations finished successfully, then the keywords will be counted.
    """
    check = True
    empty = False

    file_name = (file_path.split("/"))[len(file_path.split("/"))-1]

    # Check if size of file is 0
    if os.stat(file_path).st_size == 0 :
        empty = True
        check = False

    if empty != True :
        # Move the cursor to the end of the file
        file_obj.seek(0, os.SEEK_END)

        # Get the current position of the pointer
        pointer_location = file_obj.tell()
        
        # Create a buffer to keep the last read line
        buffer = bytearray()

        #Loop in reverse order until "Normal termination" line is found
        while pointer_location >= 0 :
            # Move the file pointer to the location pointed by the pointer
            file_obj.seek(pointer_location)

            pointer_location -= 1 # Shift pointer location back by 1
            
            new_byte = file_obj.read(1) # Read that byte/character

            if new_byte == b'\n' : # If the byte is a newline character, then the end of a line has been reached
                line = buffer.decode()[::-1] #Fetch the line from buffer
                if 'Normal termination of Gaussian 16' in line :
                    print("  File, %s, terminated normally." % file_name)
                    break
                # Reinitialize the byte array to save next line
                buffer = bytearray()
            else:
                buffer.extend(new_byte)

        # As file is read completely, if the line has not been detected then the file did not terminate normally.
        if pointer_location <= 0:
            print("  Normal termination not detected in %s." %file_name)
            check = False
    else:
        print("  File, %s, is empty." % file_name)

    return check


def extract_data(file_obj: file_wrapper) -> tuple[list[str]]: 
    # Initialize local var
    link0 = bytearray()
    route_cmds = bytearray()
    extracted = False

    # Move the cursor to the beginning of the file
    file_obj.seek(0)

    # Read first line
    line = file_obj.readline()
    while line:
        # if the line starts with a %, it is a link0 command
        if b"%" in line[:3] :
                #print("Found link0 input\n%s" % line)
                line = line.split()
                [link0.extend(b" " + elem) for elem in line if b"%" in elem and elem != b""]
        # if the line starts with a #, it's the route section line
        elif b"#" in line[:3] :
            #print("Found Route Line\n%s" % line)
            line = line.split()
            [route_cmds.extend(b" " + elem) for elem in line if b"#" not in elem and elem != b""]
            # Grab the last keyword in case line spills over
            end_keyword = line[len(line) - 1]
            # grab next line if the contents spill over
            line = file_obj.readline()
            while b'----------------------------------------------------------------------' not in line :
                line = line.split()
                # Chances are if the line spills it wrecks a keyword. This takes the last keyword
                # and combines it with the first of the next line
                if len(line) > 1 :
                    start_keyword = line[0]
                    # Add the joined keyword
                else :
                    # Extra protection against bad lines
                    break
                route_cmds.extend(b" "+end_keyword+start_keyword)
                # Extend bytearray by the additional keywords
                [route_cmds.extend(b" " + elem) for elem in line if elem != b""]
                # Read the next line
                line = file_obj.readline()
            extracted = True
        
        # Once the route section commands are collected, stop iterating over the lines in the file.
        if extracted == True:
            break
        # Iterate over the next line until the route section is collected
        line = file_obj.readline()

    return link0.decode("ascii").split(), route_cmds.decode("ascii").split()


def update_mostFreq_data(mostFreq_dict:dict[str:int], keywords:list[str]) -> None :
    """ 
    This function updates the mostFreq data used to track the most popular G16 keywords:
    Update the count if the keyword is in the dictionary.
    If the keyword is not in the dictionary, its added with a default count of 1.
    """
    [mostFreq_dict.update({elem:mostFreq_dict[elem]+1}) for elem in keywords if elem in mostFreq_dict.keys()]
    [mostFreq_dict.setdefault(elem,1) for elem in keywords if elem not in mostFreq_dict.keys()]


def replace_filename(link0_list:list,file_path:str) -> list:
    # Extract file string from the file path
    file_str = file_path.split("/")[len(file_path.split("/"))-1].replace(".log","")
    # Replace the file string with '__filename__'
    return [keyword.replace(file_str,"__filename__") for keyword in link0_list if file_str in keyword]


def order_dict(mostFreq_dict:dict[str:int]) -> tuple[str,int]:
    """Sort the data by the integer value from greatest to least"""
    return sorted(mostFreq_dict.items(),key=lambda elem: elem[1],reverse=True)


def sorted_dict(mostFreq_dict:dict[str:int]) -> dict[str:int]:
    """Sort the data by the integer value from greatest to least"""
    return dict(sorted(mostFreq_dict.items(),key=lambda elem: elem[1],reverse=True))


def export_data_json(data_path: str, link0_mostFreq: dict[str:int]=None,route_mostFreq: dict[str:int]=None) -> str :
    # Add the json extension to data_path
    data_path += ".json"
    # Organize the data into a list of dicts
    data = [link0_mostFreq,route_mostFreq]
    # Write the list of dicts to the json file
    with open(data_path,"w") as file_obj :
        json.dump(data,file_obj)
    return data_path


def main() :
    # Initialize variables
    link0_mostFreq = dict()
    route_mostFreq = dict()
    data_path = set_data_path()
    file_list = find_files_in_dir()

    # Extract data from each file and update the mostFreq dictionaries
    for file_path in file_list :
        try:
            with open(file_path,"rb") as infile :
                # Ensure normal termination of G16
                check = check_log_file(file_path=file_path,file_obj=infile)
                if check : 
                    (link0, route_cmds) = extract_data(file_obj=infile)
                    link0 = replace_filename(link0,file_path)
                    update_mostFreq_data(link0_mostFreq,link0)
                    update_mostFreq_data(route_mostFreq,route_cmds)
                else:
                    pass # Skip over files that aren't good
        # To catch all non G16 files on the computer
        except UnicodeDecodeError as ude:
            file_name = (file_path.split("/"))[len(file_path.split("/"))-1]
            print("  File, %s, %s" % (file_name,ude))
        except FileNotFoundError as fne:
            file_name = (file_path.split("/"))[len(file_path.split("/"))-1]
            print("  File, %s, %s" % (file_name,fne))

    # Order the data to be written out to the files
    route_mostFreq = sorted_dict(route_mostFreq)
    link0_mostFreq = sorted_dict(link0_mostFreq)

    # Write data to a json file
    data_path = export_data_json(data_path,link0_mostFreq,route_mostFreq)
    print("\nData recorded in file at path:\n     %s" % data_path)

main()

"""
Example of test answers

Simple data file string is:
        LogFile

Copy and past path:
        /Users/Riley/Documents/Research/User_Input_Module/

Use example files in the directory at the path:
        /Users/Riley/Documents/Research/User_Input_Module/Gaussian_Outputs_Keywords/
"""