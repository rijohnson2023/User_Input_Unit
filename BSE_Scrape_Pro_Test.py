import requests as req


def bse_url_creator(bs_name:str,version_num:str) -> str:
    # Components for the Basis Set Exchange URL.
    scheme = "https:"
    authority = "//www.basissetexchange.org"
    temp_path = "/download_basis/basis/BS_NAME/format/gaussian94/" # BS_NAME is a place holder to be replaced with each iteration
    param1 = "version="
    param2 = "elements="
    # set up the first parameter (version number)
    parameter= "".join([param1, str(version_num)])
    # correct the path with the correct basis name
    path = temp_path.replace("BS_NAME", bs_name)
    # create the url for the request
    url = "?".join(["".join([scheme, authority, path]),parameter])
    return url


def get_basis_set_object(url:str) -> tuple[bool,str]:
    """
    Takes a url and returns a bool and the basis set object.
    If the program cannot connect to basis set exchange, the basis set object with be NoneType
    """
    res = req.get(url)
    if res.status_code == req.codes.ok :
        status = True
        raw_BSO = res.text
        # separates the Basis Set Exchange title from the actual basis set.
        basis_set_object = res.text.split("!----------------------------------------------------------------------")[-1]
        # breaks contents down to the atom and creates an atom list
        basis_atoms = list()
        basis_set_funcs = basis_set_object.split("****")
        for basis_atom_funcs in basis_set_funcs:
            basis_atom_line = (basis_atom_funcs.strip()).split("\n")[0]
            if len(basis_atom_line) >= 1:
                basis_atom = basis_atom_line.split()[0]
                basis_atoms.append(basis_atom)

        # basis_set_object = raw_BSO.split("\n\n")[1]
    else :
        status = False
        basis_set_object = None
        basis_atoms = None
    return status, basis_set_object, basis_atoms


def touch_basis_set_exchange(basis_name:str,version_nums:list[int] =[0,1,2]) -> tuple[str,int]:
    # If the program cannot touch the basis set object for the basis name, then it will return None, None
    valid_version_num = None
    basis_set_object = None
    basis_atoms = None
    #Iterating over all known version numbers
    for version_num in version_nums:
        bse_url = bse_url_creator(basis_name,version_num)
        status, buffer_BSO, buffer_BSA = get_basis_set_object(bse_url)
        # Saving and updating the latest version number and basis set object
        if status == True :
            valid_version_num = version_num
            basis_set_object = buffer_BSO
            basis_atoms = buffer_BSA
    return valid_version_num, basis_set_object, basis_atoms 


def test(basis_name:str= '6-31g') -> None:
    version_num, basis_set_object, basis_atoms = touch_basis_set_exchange(basis_name)
    if version_num == None and basis_set_object == None and basis_atoms == None :
        print("Invalid Basis Name: %s" % basis_name)
    else:
        #print("Basis name: %s\nVersion number: %d\nBasis atoms:%s\nBasis set object:\n%s" % (basis_name,version_num,basis_atoms,basis_set_object))
        print("\nBasis name: %s\nVersion number: %d\nBasis atoms:%s\n" % (basis_name,version_num,basis_atoms))

#test()

def meta_test():
    basis_names = ['2zapa-nr-cv','2zapa-nr','3-21g','3zapa-nr-cv','3zapa-nr','4-31g','4zapa-nr-cv','4zapa-nr','5-21g','5zapa-nr-cv','5zapa-nr','6-21g','6-31++g','6-31++g*','6-31++g**-j','6-31++g**','6-31+g']
    for basis_name in basis_names:
        version_num, basis_set_object, basis_atoms = touch_basis_set_exchange(basis_name)
        if version_num == None and basis_set_object == None and basis_atoms == None :
            print("INVALID INPUTS:\nBasis name: %s\nVersion number: %d\nBasis atoms:%s\n" % (basis_name,version_num,basis_atoms))
        else:
            print("\nBasis name: %s\nVersion number: %d\nBasis atoms:%s\n" % (basis_name,version_num,basis_atoms))


meta_test()