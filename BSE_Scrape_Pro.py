from asyncore import file_wrapper
import os
import json
import requests as req
from Apps import PeriodicTable as PT


def set_data_path() -> str:
    outfile_name = input("Name the file to store the data:\n(Do not include the extension)\n")

    # Locate current working directory as destination for report
    data_path = os.path.join(os.getcwd(),outfile_name)

    while True :
        # Two answers: acceptable: 1. path, 2. "", all else are bad"
        answer = str(input("The data recorded will be at path:\n%10s\nHit enter to proceed, or type new path without '/LogData.csv':\n  " % data_path))
        if answer == "" :
            break
        elif os.path.isdir(answer) :
            data_path = os.path.join(answer,outfile_name)
            break

    return data_path


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


def export_data_json(data_path: str, data: dict[str:[int,list[int]]]=None,route_mostFreq: dict[str:int]=None) -> str :
    # Add the json extension to data_path
    data_path += ".json"
    # Write the list of dicts to the json file
    with open(data_path,"w") as file_obj :
        json.dump(data,file_obj)
    return data_path


def basis_iterator(basis_name:str, BSE_Data:dict, record_obj: file_wrapper) -> None :
    version_num, basis_set_object, basis_atoms = touch_basis_set_exchange(basis_name)
    if version_num == None :
        message = "\nINVALID INPUTS:\nBasis name: %s\nVersion number: %s\nBasis atoms: %s\n" % (basis_name,str(version_num),str(basis_atoms))
    else:
        message = "\nBasis name: %s\nVersion number: %d\nBasis atoms: %s\n" % (basis_name,version_num,basis_atoms)
        # Add contents to dictionary
        atom_nums = [PT.getNumber(basis_atom) for basis_atom in basis_atoms]
        BSE_Data[basis_name] = [version_num,atom_nums]
    # Write message in human readable format into the txt file
    record_obj.write(message)
    print(message)


def main() :
    BSE_Data = dict()
    data_path = set_data_path()
    data_record = data_path + ".txt"
    with open(data_record,"w") as record_obj :
        for basis_name in basis_names:
            basis_iterator(basis_name,BSE_Data,record_obj)
    export_data_json(data_path,BSE_Data)
    

# Basis Names
basis_names = ['2zapa-nr-cv','2zapa-nr','3-21g','3zapa-nr-cv','3zapa-nr','4-31g','4zapa-nr-cv','4zapa-nr','5-21g','5zapa-nr-cv','5zapa-nr','6-21g','6-31++g','6-31++g*','6-31++g**-j','6-31++g**','6-31+g','6-31+g*-j','6-31+g*','6-31+g**','6-311++g(2d,2p)','6-311++g(3df,3pd)','6-311++g','6-311++g*','6-311++g**-j','6-311++g**','6-311+g(2d,p)','6-311+g','6-311+g*-j','6-311+g*','6-311+g**','6-311g(2df,2pd)','6-311g(d,p)','6-311g-j','6-311g','6-311g*','6-311g**-rifit','6-311g**','6-311xxg(d,p)','6-31g(2df,p)','6-31g(3df,3pd)','6-31g(d,p)','6-31g-blaudeau','6-31g-j','6-31g','6-31g*-blaudeau','6-31g*','6-31g**-rifit','6-31g**','6zapa-nr','7zapa-nr','acv2z-j','acv3z-j','acv4z-j','admm-1','admm-2','admm-3','ahgbs-5','ahgbs-7','ahgbs-9','ahgbsp1-5','ahgbsp1-7','ahgbsp1-9','ahgbsp2-5','ahgbsp2-7','ahgbsp2-9','ahgbsp3-5','ahgbsp3-7','ahgbsp3-9','ahlrichs pvdz','ahlrichs tzv','ahlrichs vdz','ahlrichs vtz','ano-dk3','ano-r','ano-r0','ano-r1','ano-r2','ano-r3','ano-rcc-mb','ano-rcc-vdz','ano-rcc-vdzp','ano-rcc-vqzp','ano-rcc-vtz','ano-rcc-vtzp','ano-rcc','ano-vt-dz','ano-vt-qz','ano-vt-tz','apr-cc-pv(q+d)z','atzp-zora','aug-admm-1','aug-admm-2','aug-admm-3','aug-cc-pcv5z','aug-cc-pcvdz-dk','aug-cc-pcvdz','aug-cc-pcvqz-dk','aug-cc-pcvqz','aug-cc-pcvtz-dk','aug-cc-pcvtz','aug-cc-pv(5+d)z','aug-cc-pv(d+d)z','aug-cc-pv(q+d)z','aug-cc-pv(t+d)z','aug-cc-pv5z-dk','aug-cc-pv5z-optri','aug-cc-pv5z-pp-optri','aug-cc-pv5z-pp-rifit','aug-cc-pv5z-pp','aug-cc-pv5z-rifit','aug-cc-pv5z','aug-cc-pv6z-rifit','aug-cc-pv6z','aug-cc-pv7z','aug-cc-pvdz-dk','aug-cc-pvdz-dk3','aug-cc-pvdz-optri','aug-cc-pvdz-pp-optri','aug-cc-pvdz-pp-rifit','aug-cc-pvdz-pp','aug-cc-pvdz-rifit','aug-cc-pvdz-x2c','aug-cc-pvdz','aug-cc-pvqz-dk','aug-cc-pvqz-dk3','aug-cc-pvqz-optri','aug-cc-pvqz-pp-optri','aug-cc-pvqz-pp-rifit','aug-cc-pvqz-pp','aug-cc-pvqz-rifit','aug-cc-pvqz-x2c','aug-cc-pvqz','aug-cc-pvtz-dk','aug-cc-pvtz-dk3','aug-cc-pvtz-j','aug-cc-pvtz-optri','aug-cc-pvtz-pp-optri','aug-cc-pvtz-pp-rifit','aug-cc-pvtz-pp','aug-cc-pvtz-rifit','aug-cc-pvtz-x2c','aug-cc-pvtz','aug-cc-pwcv5z-dk','aug-cc-pwcv5z-pp-optri','aug-cc-pwcv5z-pp-rifit','aug-cc-pwcv5z-pp','aug-cc-pwcv5z-rifit','aug-cc-pwcv5z','aug-cc-pwcvdz-dk3','aug-cc-pwcvdz-pp-optri','aug-cc-pwcvdz-pp-rifit','aug-cc-pwcvdz-pp','aug-cc-pwcvdz-rifit','aug-cc-pwcvdz-x2c','aug-cc-pwcvdz','aug-cc-pwcvqz-dk','aug-cc-pwcvqz-dk3','aug-cc-pwcvqz-pp-optri','aug-cc-pwcvqz-pp-rifit','aug-cc-pwcvqz-pp','aug-cc-pwcvqz-rifit','aug-cc-pwcvqz-x2c','aug-cc-pwcvqz','aug-cc-pwcvtz-dk','aug-cc-pwcvtz-dk3','aug-cc-pwcvtz-pp-optri','aug-cc-pwcvtz-pp-rifit','aug-cc-pwcvtz-pp','aug-cc-pwcvtz-rifit','aug-cc-pwcvtz-x2c','aug-cc-pwcvtz','aug-ccx-5z','aug-ccx-dz','aug-ccx-qz','aug-ccx-tz','aug-mcc-pv5z','aug-mcc-pv6z','aug-mcc-pv7z','aug-mcc-pv8z','aug-mcc-pvqz','aug-mcc-pvtz','aug-pc-0','aug-pc-1','aug-pc-2','aug-pc-3','aug-pc-4','aug-pch-1','aug-pch-2','aug-pch-3','aug-pch-4','aug-pcj-0','aug-pcj-0_2006','aug-pcj-1','aug-pcj-1_2006','aug-pcj-2','aug-pcj-2_2006','aug-pcj-3','aug-pcj-3_2006','aug-pcj-4','aug-pcj-4_2006','aug-pcs-0','aug-pcs-1','aug-pcs-2','aug-pcs-3','aug-pcs-4','aug-pcseg-0','aug-pcseg-1','aug-pcseg-2','aug-pcseg-3','aug-pcseg-4','aug-pcsseg-0','aug-pcsseg-1','aug-pcsseg-2','aug-pcsseg-3','aug-pcsseg-4','aug-pcx-1','aug-pcx-2','aug-pcx-3','aug-pcx-4','aug-pv7z','binning 641(d)','binning 641(df)','binning 641+(d)','binning 641+(df)','binning 641+','binning 641','binning 962(d)','binning 962(df)','binning 962+(d)','binning 962+(df)','binning 962+','binning 962','cc-pcv5z','cc-pcvdz-dk','cc-pcvdz-f12-optri','cc-pcvdz-f12-rifit','cc-pcvdz-f12','cc-pcvdz','cc-pcvqz-dk','cc-pcvqz-f12-optri','cc-pcvqz-f12-rifit','cc-pcvqz-f12','cc-pcvqz','cc-pcvtz-dk','cc-pcvtz-f12-optri','cc-pcvtz-f12-rifit','cc-pcvtz-f12','cc-pcvtz','cc-pv(5+d)z','cc-pv(d+d)z','cc-pv(q+d)z','cc-pv(t+d)z','cc-pv5z(fi/sf/fw)','cc-pv5z(fi/sf/lc)','cc-pv5z(fi/sf/sc)','cc-pv5z(pt/sf/fw)','cc-pv5z(pt/sf/lc)','cc-pv5z(pt/sf/sc)','cc-pv5z-dk','cc-pv5z-f12(rev2)','cc-pv5z-f12','cc-pv5z-jkfit','cc-pv5z-pp-rifit','cc-pv5z-pp','cc-pv5z-rifit','cc-pv5z','cc-pv6z-rifit','cc-pv6z','cc-pv8z','cc-pv9z','cc-pvdz(fi/sf/fw)','cc-pvdz(fi/sf/lc)','cc-pvdz(fi/sf/sc)','cc-pvdz(pt/sf/fw)','cc-pvdz(pt/sf/lc)','cc-pvdz(pt/sf/sc)','cc-pvdz(seg-opt)','cc-pvdz-dk','cc-pvdz-dk3','cc-pvdz-f12(rev2)','cc-pvdz-f12-optri','cc-pvdz-f12','cc-pvdz-pp-rifit','cc-pvdz-pp','cc-pvdz-rifit','cc-pvdz-x2c','cc-pvdz','cc-pvqz(fi/sf/fw)','cc-pvqz(fi/sf/lc)','cc-pvqz(fi/sf/sc)','cc-pvqz(pt/sf/fw)','cc-pvqz(pt/sf/lc)','cc-pvqz(pt/sf/sc)','cc-pvqz(seg-opt)','cc-pvqz-dk','cc-pvqz-dk3','cc-pvqz-f12(rev2)','cc-pvqz-f12-optri','cc-pvqz-f12','cc-pvqz-jkfit','cc-pvqz-pp-rifit','cc-pvqz-pp','cc-pvqz-rifit','cc-pvqz-x2c','cc-pvqz','cc-pvtz(fi/sf/fw)','cc-pvtz(fi/sf/lc)','cc-pvtz(fi/sf/sc)','cc-pvtz(pt/sf/fw)','cc-pvtz(pt/sf/lc)','cc-pvtz(pt/sf/sc)','cc-pvtz(seg-opt)','cc-pvtz-dk','cc-pvtz-dk3','cc-pvtz-f12(rev2)','cc-pvtz-f12-optri','cc-pvtz-f12','cc-pvtz-jkfit','cc-pvtz-pp-rifit','cc-pvtz-pp','cc-pvtz-rifit','cc-pvtz-x2c','cc-pvtz','cc-pwcv5z-dk','cc-pwcv5z-pp-rifit','cc-pwcv5z-pp','cc-pwcv5z-rifit','cc-pwcv5z','cc-pwcvdz-dk3','cc-pwcvdz-pp-rifit','cc-pwcvdz-pp','cc-pwcvdz-rifit','cc-pwcvdz-x2c','cc-pwcvdz','cc-pwcvqz-dk','cc-pwcvqz-dk3','cc-pwcvqz-pp-rifit','cc-pwcvqz-pp','cc-pwcvqz-rifit','cc-pwcvqz-x2c','cc-pwcvqz','cc-pwcvtz-dk','cc-pwcvtz-dk3','cc-pwcvtz-pp-rifit','cc-pwcvtz-pp','cc-pwcvtz-rifit','cc-pwcvtz-x2c','cc-pwcvtz','ccemd-2','ccemd-3','ccj-pv5z','ccj-pvdz','ccj-pvqz','ccj-pvtz','ccx-5z','ccx-dz','ccx-qz','ccx-tz','coemd-2','coemd-3','coemd-4','coemd-ref','cologne dkh2','crenbl ecp','crenbl','crenbs ecp','crenbs','d-aug-cc-pv5z','d-aug-cc-pv6z','d-aug-cc-pvdz','d-aug-cc-pvqz','d-aug-cc-pvtz','def2-ecp','def2-qzvp-rifit','def2-qzvp','def2-qzvpd','def2-qzvpp-rifit','def2-qzvpp','def2-qzvppd-rifit','def2-qzvppd','def2-sv(p)-jkfit','def2-sv(p)-rifit','def2-sv(p)','def2-svp-rifit','def2-svp','def2-svpd-rifit','def2-svpd','def2-tzvp-rifit','def2-tzvp','def2-tzvpd-rifit','def2-tzvpd','def2-tzvpp-rifit','def2-tzvpp','def2-tzvppd-rifit','def2-tzvppd','def2-universal-jfit','def2-universal-jkfit','demon2k-dzvp-gga','dfo+-nrlmol','dfo-1-bhs','dfo-1','dfo-2','dfo-nrlmol','dgauss-a1-dftjfit','dgauss-a1-dftxfit','dgauss-a2-dftjfit','dgauss-a2-dftxfit','dgauss-dzvp','dgauss-dzvp2','dgauss-tzvp','dhf-ecp','dhf-qzvp','dhf-qzvpp','dhf-sv(p)','dhf-svp','dhf-tzvp','dhf-tzvpp','dz (dunning-hay)','dz + double rydberg (dunning-hay)','dz + rydberg (dunning-hay)','dzp (dunning-hay)','dzp + diffuse (dunning-hay)','dzp + rydberg (dunning-hay)','fano-5z','fano-6z','fano-dz','fano-qz','fano-tz','hgbs-5','hgbs-7','hgbs-9','hgbsp1-5','hgbsp1-7','hgbsp1-9','hgbsp2-5','hgbsp2-7','hgbsp2-9','hgbsp3-5','hgbsp3-7','hgbsp3-9','iglo-ii','iglo-iii','jgauss-dzp','jgauss-qz2p','jgauss-qzp','jgauss-tzp1','jgauss-tzp2','jorge-5zp-dkh','jorge-5zp','jorge-6zp-dkh','jorge-6zp','jorge-a5zp','jorge-adzp','jorge-aqzp','jorge-atzp','jorge-dzp-dkh','jorge-dzp','jorge-qzp-dkh','jorge-qzp','jorge-tzp-dkh','jorge-tzp','jul-cc-pv(d+d)z','jul-cc-pv(q+d)z','jul-cc-pv(t+d)z','jun-cc-pv(d+d)z','jun-cc-pv(q+d)z','jun-cc-pv(t+d)z','koga unpolarized','lanl08(d)','lanl08(f)','lanl08+','lanl08','lanl2dz ecp','lanl2dz','lanl2dzdp','lanl2tz(f)','lanl2tz+','lanl2tz','m6-31g','m6-31g*','maug-cc-pv(d+d)z','maug-cc-pv(q+d)z','maug-cc-pv(t+d)z','may-cc-pv(q+d)z','may-cc-pv(t+d)z','midi!','midi','midix','mini','modified-lanl2dz','nasa ames ano','nasa ames ano2','nasa ames cc-pcv5z','nasa ames cc-pcvqz','nasa ames cc-pcvtz','nasa ames cc-pv5z','nasa ames cc-pvqz','nasa ames cc-pvtz','nlo-v','nmr-dkh (tz2p)','orp','partridge uncontracted 1','partridge uncontracted 2','partridge uncontracted 3','partridge uncontracted 4','pc-0','pc-1','pc-2','pc-3','pc-4','pcemd-2','pcemd-3','pcemd-4','pch-1','pch-2','pch-3','pch-4','pcj-0','pcj-0_2006','pcj-1','pcj-1_2006','pcj-2','pcj-2_2006','pcj-3','pcj-3_2006','pcj-4','pcj-4_2006','pcs-0','pcs-1','pcs-2','pcs-3','pcs-4','pcseg-0','pcseg-1','pcseg-2','pcseg-3','pcseg-4','pcsseg-0','pcsseg-1','pcsseg-2','pcsseg-3','pcsseg-4','pcx-1','pcx-2','pcx-3','pcx-4','psbkjc','pt - mdzp','pv6z','pv7z','roos augmented double zeta ano','roos augmented triple zeta ano','s3-21g','s3-21g*','s6-31g','s6-31g*','sadlej pvtz','sadlej+','sap_grasp_large','sap_grasp_small','sap_helfem_large','sap_helfem_small','sapporo-dkh3-dzp-2012-diffuse','sapporo-dkh3-dzp-2012','sapporo-dkh3-dzp-diffuse','sapporo-dkh3-dzp','sapporo-dkh3-qzp-2012-diffuse','sapporo-dkh3-qzp-2012','sapporo-dkh3-qzp-diffuse','sapporo-dkh3-qzp','sapporo-dkh3-tzp-2012-diffuse','sapporo-dkh3-tzp-2012','sapporo-dkh3-tzp-diffuse','sapporo-dkh3-tzp','sapporo-dzp-2012-diffuse','sapporo-dzp-2012','sapporo-dzp-diffuse','sapporo-dzp','sapporo-qzp-2012-diffuse','sapporo-qzp-2012','sapporo-qzp-diffuse','sapporo-qzp','sapporo-tzp-2012-diffuse','sapporo-tzp-2012','sapporo-tzp-diffuse','sapporo-tzp','sarc-dkh2','sarc-zora','sarc2-qzv-dkh2-jkfit','sarc2-qzv-dkh2','sarc2-qzv-zora-jkfit','sarc2-qzv-zora','sarc2-qzvp-dkh2-jkfit','sarc2-qzvp-dkh2','sarc2-qzvp-zora-jkfit','sarc2-qzvp-zora','sbkjc polarized (p,2d) - lfk','sbkjc-ecp','sbkjc-vdz','sbo4-dz(d)-3g','sbo4-dz(d,p)-3g','sbo4-sz-3g','scaled mini','sto-2g','sto-3g','sto-3g*','sto-4g','sto-5g','sto-6g','stuttgart rlc ecp','stuttgart rlc','stuttgart rsc 1997 ecp','stuttgart rsc 1997','stuttgart rsc ano','stuttgart rsc segmented + ecp','sv (dunning-hay)','sv + double rydberg (dunning-hay)','sv + rydberg (dunning-hay)','svp (dunning-hay)','svp + diffuse (dunning-hay)','svp + diffuse + rydberg (dunning-hay)','svp + rydberg (dunning-hay)','tz (dunning-hay)','tzp-zora','ugbs','un-ccemd-ref','un-pcemd-ref','wachters+f','wtbs','x2c-jfit-universal','x2c-jfit','x2c-qzvpall-2c-s','x2c-qzvpall-2c','x2c-qzvpall-s','x2c-qzvpall','x2c-qzvppall-2c-s','x2c-qzvppall-2c','x2c-qzvppall-s','x2c-qzvppall','x2c-sv(p)all-2c','x2c-sv(p)all-s','x2c-sv(p)all','x2c-svpall-2c','x2c-svpall-s','x2c-svpall','x2c-tzvpall-2c','x2c-tzvpall-s','x2c-tzvpall','x2c-tzvppall-2c','x2c-tzvppall-s','x2c-tzvppall']

main()