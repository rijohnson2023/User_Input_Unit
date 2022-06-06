
#!/opt/anaconda3/bin/env python
import requests as req
from ModifierData import *


# Components for the Basis Set Exchange URL.
scheme = "https:"
authority = "//www.basissetexchange.org"
temp_path = "/download_basis/basis/BS_NAME/format/gaussian94/" # BS_NAME is a place holder to be replaced with each iteration
param1 = "version="
param2 = "elements="


##
# creates a url for a unique basis set name
# @ param : bs_name - name of the basis set,
# @ return: properly formatted url for basis set exchange
def urlCreator(bs_name) :
    # aquire the version from the array
    version = str(BSE_VERSIONNUMBERS[bs_name])
    # set up the first parameter (version number)
    parameter= "".join([param1, version])
    # correct the path with the correct basis name
    path = temp_path.replace("BS_NAME", bs_name)
    # create the url for the request
    url = "?".join(["".join([scheme, authority, path]),parameter])

    return url, int(version)


##
# @ param: 
# @ return:  
def touchWeb(url) :
    res = req.get(url)
    if res.status_code == req.codes.ok :
        status = True
    else :
        status = False
    return status


def main() :
    Record = dict()
    totalTouches = 0
    successes = 0
    failures = 0

    with open("BasisSetExchange_URL_Test.txt", "w") as file : # Open and create file to log data
        for bs_name in BSE_VERSIONNUMBERS : # Iterate over all basis set names available on Basis Set Exchange

            print("%30s" % bs_name, end = ":") # Notify user what basis set name is being tested

            url, version = urlCreator(bs_name) # Create url and touch www.basissetexchange.org

            status = touchWeb(url) # touching the url to see if it exists

            line = "%s;%i;%s;%s;\n" % (bs_name, version, str(status), url) # creating a line to write to the log file

            file.write(line) # writing the line to the log file

            totalTouches += 1 # Incrementing the count for totalTouches

            # Notifying the user of the success of the touch
            if status is True :
                print("%20s" % "Succeeded")
                successes += 1
            else :
                failures += 1
                print("%20s" % "Failed")

        # Calculating the success rate and the fail failrate
        successRate = float(successes/totalTouches) * 100
        failRate = float(failures/totalTouches) * 100

        # Writing out a summary of the data at the bottom of the file
        line1 = "Succcess Rate : %4.4f" % successRate
        line2 = "Fail Rate :     %4.4f" % failRate
        line3 = "Total Web Touches: %4d" % totalTouches

        # Joining the lines into a single string
        Footer = ";\n".join(["*"*5,line1,line2,line3,"*"*5])
        Footer = Footer + ";\n"

        # Writing the contents into the textfile
        file.write(Footer)

main()

