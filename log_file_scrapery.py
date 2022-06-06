from asyncore import file_wrapper
import os, sys
import pprint as pp

def set_data_path() -> str:
    # Locate current working directory as destination for report
    data_path = os.path.join(os.getcwd(),"LogData.csv")

    while True :
        # Two answers: acceptable: 1. path, 2. "", all else are bad"
        answer = str(input("The data recorded will be at path:\n%10s\nHit enter to proceed, or type new path without '/LogData.csv':\n  " % data_path))
        if answer == "" :
            break
        elif os.path.isdir(answer) :
            data_path = os.path.join(answer,"LogData.csv")
            break

    return data_path

def find_file_in_dir() -> list[str] :
    # Get valid source directory from user
    source_dir = input("Please input the directory path to search:\n")
    while not os.path.isdir(source_dir) :
        source_dir = input("Invalid path, enter a new directory path to search:\n")

    # Create a list of all the log files in the directory
    listoffiles = list()
    for (dirpath, dir_names, filenames) in os.walk(source_dir):
        listoffiles += [os.path.join(dirpath,file) for file in filenames if file.split(".")[len(file.split("."))-1] == "log"]

    print("%d log files were found in the directory branch:\n%s" % (len(listoffiles), source_dir))
    return listoffiles

def check_log_file(file_path: str, file_obj: file_wrapper) -> bool:
    check = True

    # Check if size of file is 0
    if os.stat(file_path).st_size == 0 :
        print('File is empty:')
        check = False

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
                print("File terminated normally.")
                break
            # Reinitialize the byte array to save next line
            buffer = bytearray()
        else:
            buffer.extend(new_byte)

    # As file is read completely, if the line has not been detected then the file did not terminate normally.
    if pointer_location <= 0:
        print("Normal termination not detected.")
        check = False

    return check

def extract_data(file_obj: file_wrapper) -> tuple:
    # Initialize local var
    link0 = bytearray()
    route_cmds = bytearray()

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
            # grab next line if the contents spill over
            line = file_obj.readline()
            while line :
                if b'----------------------------------------------------------------------' in line :
                    break
                line = line.split()
                [route_cmds.extend(b" " + elem) for elem in line if elem != b""]
                line = file_obj.readline()
            break
        line = file_obj.readline()

    return link0.decode("ascii"), route_cmds.decode("ascii")

def main() :
    with open(file_path1,"rb") as infile :
        check = check_log_file(file_path=file_path1,file_obj=infile)
        if check : 
            #pass
            (link0, route_cmds) = extract_data(file_obj=infile)
            print(link0)
            print(route_cmds)

file_path1 = '/Users/Riley/Documents/Research/User_Input_Module/Gaussian_Outputs_Keywords/AllylChloride.log'
file_path2 = '/Users/Riley/Documents/Research/User_Input_Module/Gaussian_Outputs_Keywords/NotNormalTerm.log'
file_path3 = '/Users/Riley/Documents/Research/User_Input_Module/Gaussian_Outputs_Keywords/EmptyFile.log'
data_path = '/Users/Riley/Documents/Research/User_Input_Module/LogData.csv'

main()