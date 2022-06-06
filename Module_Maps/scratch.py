"""
Each file needs to have the string

'Normal termination of Gaussian 16'
 Normal termination of Gaussian 16 at Tue Jun 25 15:59:25 2019.

Grab the header section of the file.

link0 commands

Route section commands
"""

# Example 1
"""

file_path: /Volumes/Soul_Power/Christus/Riley_Research/lab6practice/AllylChlorideClTS.log

 ******************************************
 Gaussian 16:  ES64L-G16RevA.03 25-Dec-2016
                10-May-2021 
 ******************************************
 %oldchk=AllylChlorideClTS.chk
 %chk=AllylChlorideClTS-TS.chk
 Copying data from "AllylChlorideClTS.chk" to current chk file "AllylChlorideClTS-TS.chk"
 IOpt=  2 FromEx=T IUOpen= 4 IOptOp= 5 NList=   0 IFRang= 0 IUIn= 4 IUOut= 2.
 ----------------------------------------------------------------------
 # opt=(ts,noeigen,readfc,modredundant) freq hf/3-21g scrf=(smd,solvent
 =dmso) nosymm geom=checkpoint guess=read
 ----------------------------------------------------------------------
"""

#Example 2
"""

file_path: /Volumes/Soul_Power/Christus/Riley_Research/lab6practice/Cl.log

 ******************************************
 Gaussian 16:  ES64L-G16RevA.03 25-Dec-2016
                10-May-2021 
 ******************************************
 %chk=Cl.chk
 ---------------------------------------------------------
 # freq hf/3-21g scrf=(smd,solvent=dmso) geom=connectivity
 ---------------------------------------------------------
"""

#Example 3
"""

file path: /Volumes/Soul_Power/Christus/Riley_Research/lab6practice/AllylChloride.log                             

 ******************************************
 Gaussian 16:  ES64L-G16RevA.03 25-Dec-2016
                10-May-2021 
 ******************************************
 %chk=AllylChloride.chk
 %nprocs=60
 Will use up to   60 processors via shared memory.
 %mem=60GB
 ----------------------------------------------------------------------
 # opt=(maxcycles=85) freq=noraman hf/3-21g scrf=(smd,solvent=dmso) geo
 m=connectivity
 ----------------------------------------------------------------------
"""

# Example 4
"""

file_path: /Volumes/Soul_Power/Christus/Gaussian/Beta/Pd2p-ene/CO/transcis/P/Pd2p-ene-CO-transcis-P-fromciscis.log

 ******************************************
 Gaussian 16:  ES64L-G16RevA.03 25-Dec-2016
                25-Jun-2019 
 ******************************************
 %nprocshared=60
 Will use up to   60 processors via shared memory.
 %mem=60GB
 %chk=Pd2p-ene-CO-transcis-P-fromciscis.chk
 ----------------------------------------------------------------------
 # opt=maxcycles=85 freq=noraman b3lyp/gen scrf=(smd,solvent=water) nos
 ymm geom=connectivity pseudo=read
 ----------------------------------------------------------------------
 """