"""
PeriodicTable.py contains data about the full names, symbols, atomic numbers, and atomic masses of all 118 elements.
It also contains a list of basis set versions from basissetexchange.org.

Lastly, it contains 3 functions for converting between an atom's name, symbol, and atomic number (case insensitive,
returns names and symbols as lower case), as well as a function which returns the atomic mass of an atom given its name,
symbol, or atomic number (case insensitive).
"""

# Westmont Computational Chemistry ToolKit © 2022 by Riley Johnson, Curtis Barnhart is licensed under CC BY-NC-SA 4.0
# https://github.com/rijohnson2023/MOD
# http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1

NAMES = ['actinium', 'aluminum', 'americium', 'antimony', 'argon', 'arsenic', 'astatine', 'barium', 'berkelium',
         'beryllium', 'bismuth', 'bohrium', 'boron', 'bromine', 'cadmium', 'calcium', 'californium', 'carbon', 'cerium',
         'cesium', 'chlorine', 'chromium', 'cobalt', 'copernicium', 'copper', 'curium', 'darmstadtium', 'dubnium',
         'dysprosium', 'einsteinium', 'erbium', 'europium', 'fermium', 'flerovium', 'fluorine', 'francium',
         'gadolinium', 'gallium', 'germanium', 'gold', 'hafnium', 'hassium', 'helium', 'holmium', 'hydrogen', 'indium',
         'iodine', 'iridium', 'iron', 'krypton', 'lanthanum', 'lawrencium', 'lead', 'lithium', 'livermorium',
         'lutetium', 'magnesium', 'manganese', 'meitnerium', 'mendelevium', 'mercury', 'molybdenum', 'moscovium',
         'neodymium', 'neon', 'neptunium', 'nickel', 'nihonium', 'niobium', 'nitrogen', 'nobelium', 'oganesson',
         'osmium', 'oxygen', 'palladium', 'phosphorus', 'platinum', 'plutonium', 'polonium', 'potassium',
         'praseodymium', 'promethium', 'protactinium', 'radium', 'radon', 'rhenium', 'rhodium', 'roentgenium',
         'rubidium', 'ruthenium', 'rutherfordium', 'samarium', 'scandium', 'seaborgium', 'selenium', 'silicon',
         'silver', 'sodium', 'strontium', 'sulfur', 'tantalum', 'technetium', 'tellurium', 'tennessine', 'terbium',
         'thallium', 'thorium', 'thulium', 'tin', 'titanium', 'tungsten', 'uranium', 'vanadium', 'xenon', 'ytterbium',
         'yttrium', 'zinc', 'zirconium']
SYMBOLS = ['ac', 'al', 'am', 'sb', 'ar', 'as', 'at', 'ba', 'bk', 'be', 'bi', 'bh', 'b', 'br', 'cd', 'ca', 'cf', 'c',
           'ce', 'cs', 'cl', 'cr', 'co', 'cn', 'cu', 'cm', 'ds', 'db', 'dy', 'es', 'er', 'eu', 'fm', 'fl', 'f', 'fr',
           'gd', 'ga', 'ge', 'au', 'hf', 'hs', 'he', 'ho', 'h', 'in', 'i', 'ir', 'fe', 'kr', 'la', 'lr', 'pb', 'li',
           'lv', 'lu', 'mg', 'mn', 'mt', 'md', 'hg', 'mo', 'mc', 'nd', 'ne', 'np', 'ni', 'nh', 'nb', 'n', 'no', 'og',
           'os', 'o', 'pd', 'p', 'pt', 'pu', 'po', 'k', 'pr', 'pm', 'pa', 'ra', 'rn', 're', 'rh', 'rg', 'rb', 'ru',
           'rf', 'sm', 'sc', 'sg', 'se', 'si', 'ag', 'na', 'sr', 's', 'ta', 'tc', 'te', 'ts', 'tb', 'tl', 'th', 'tm',
           'sn', 'ti', 'w', 'u', 'v', 'xe', 'yb', 'y', 'zn', 'zr']
NUMBERS = [89, 13, 95, 51, 18, 33, 85, 56, 97, 4, 83, 107, 5, 35, 48, 20, 98, 6, 58, 55, 17, 24, 27, 112, 29, 96, 110,
           105, 66, 99, 68, 63, 100, 114, 9, 87, 64, 31, 32, 79, 72, 108, 2, 67, 1, 49, 53, 77, 26, 36, 57, 103, 82, 3,
           116, 71, 12, 25, 109, 101, 80, 42, 115, 60, 10, 93, 28, 113, 41, 7, 102, 118, 76, 8, 46, 15, 78, 94, 84, 19,
           59, 61, 91, 88, 86, 75, 45, 111, 37, 44, 104, 62, 21, 106, 34, 14, 47, 11, 38, 16, 73, 43, 52, 117, 65, 81,
           90, 69, 50, 22, 74, 92, 23, 54, 70, 39, 30, 40]
MASS = [227.0, 26.982, 243.0, 121.76, 39.95, 74.922, 210.0, 137.33, 247.0, 9.012, 208.98, 270.0, 10.81, 79.904, 112.41,
        132.91, 40.078, 251.0, 12.011, 140.12, 35.45, 51.996, 58.933, 285.0, 63.546, 247.0, 281.0, 268.0, 162.5, 252.0,
        167.26, 151.96, 257.0, 289.0, 18.998, 223.0, 157.25, 69.723, 72.63, 107.87, 178.49, 277.0, 4.002, 164.93, 1.008,
        114.82, 126.9, 192.22, 55.845, 83.798, 138.91, 266.0, 207.2, 6.94, 293.0, 174.97, 24.305, 54.938, 278.0, 258.0,
        200.59, 95.95, 290.0, 144.24, 20.18, 237.0, 58.693, 286.0, 92.906, 14.007, 259.0, 294.0, 190.23, 15.999, 106.42,
        30.974, 195.08, 244.0, 209.0, 39.098, 140.91, 145.0, 231.04, 226.0, 222.0, 75.0, 102.91, 282.0, 85.468, 101.07,
        267.0, 150.36, 44.956, 269.0, 78.971, 28.085, 107.87, 22.99, 87.62, 32.06, 180.95, 98.0, 127.6, 294.0, 158.93,
        204.38, 232.04, 168.93, 118.71, 47.867, 183.84, 238.03, 50.942, 131.29, 173.05, 88.906, 65.38, 91.224]
BSE_VERSIONS = {'sdd': 0, '2zapa-nr-cv': 1, '2zapa-nr': 1, '3-21g': 1, '3zapa-nr-cv': 1, '3zapa-nr': 1,
                '4-31g': 1, '4zapa-nr-cv': 1, '4zapa-nr': 1, '5-21g': 1, '5zapa-nr-cv': 1, '5zapa-nr': 1,
                '6-21g': 1, '6-31++g': 1, '6-31++g*': 1, '6-31++g**-j': 0, '6-31++g**': 1, '6-31+g': 1,
                '6-31+g*-j': 0, '6-31+g*': 1, '6-31+g**': 1, '6-311++g(2d,2p)': 0, '6-311++g(3df,3pd)': 0,
                '6-311++g': 0, '6-311++g*': 0, '6-311++g**-j': 0, '6-311++g**': 0, '6-311+g(2d,p)': 0,
                '6-311+g': 0, '6-311+g*-j': 0, '6-311+g*': 0, '6-311+g**': 0, '6-311g(2df,2pd)': 0,
                '6-311g(d,p)': 0, '6-311g-j': 0, '6-311g': 0, '6-311g*': 0, '6-311g**-rifit': 1, '6-311g**': 0,
                '6-311xxg(d,p)': 1, '6-31g(2df,p)': 0, '6-31g(3df,3pd)': 0, '6-31g(d,p)': 1, '6-31g-blaudeau': 0,
                '6-31g-j': 0, '6-31g': 1, '6-31g*-blaudeau': 0, '6-31g*': 1, '6-31g**-rifit': 1, '6-31g**': 1,
                '6zapa-nr': 1, '7zapa-nr': 1, 'acv2z-j': 1, 'acv3z-j': 1, 'acv4z-j': 1, 'admm-1': 1, 'admm-2': 1,
                'admm-3': 1, 'ahgbs-5': 1, 'ahgbs-7': 1, 'ahgbs-9': 1, 'ahgbsp1-5': 1, 'ahgbsp1-7': 1,
                'ahgbsp1-9': 1, 'ahgbsp2-5': 1, 'ahgbsp2-7': 1, 'ahgbsp2-9': 1, 'ahgbsp3-5': 1, 'ahgbsp3-7': 1,
                'ahgbsp3-9': 1, 'ahlrichs pvdz': 0, 'ahlrichs tzv': 0, 'ahlrichs vdz': 0, 'ahlrichs vtz': 0,
                'ano-dk3': 1, 'ano-r': 2, 'ano-r0': 2, 'ano-r1': 2, 'ano-r2': 2, 'ano-r3': 2, 'ano-rcc-mb': 1,
                'ano-rcc-vdz': 1, 'ano-rcc-vdzp': 1, 'ano-rcc-vqzp': 1, 'ano-rcc-vtz': 1, 'ano-rcc-vtzp': 1,
                'ano-rcc': 1, 'ano-vt-dz': 1, 'ano-vt-qz': 2, 'ano-vt-tz': 1, 'apr-cc-pv(q+d)z': 0,
                'atzp-zora': 1, 'aug-admm-1': 1, 'aug-admm-2': 1, 'aug-admm-3': 1, 'aug-cc-pcv5z': 0,
                'aug-cc-pcvdz-dk': 0, 'aug-cc-pcvdz': 0, 'aug-cc-pcvqz-dk': 0, 'aug-cc-pcvqz': 0,
                'aug-cc-pcvtz-dk': 0, 'aug-cc-pcvtz': 0, 'aug-cc-pv(5+d)z': 1, 'aug-cc-pv(d+d)z': 1,
                'aug-cc-pv(q+d)z': 1, 'aug-cc-pv(t+d)z': 1, 'aug-cc-pv5z-dk': 0, 'aug-cc-pv5z-optri': 0,
                'aug-cc-pv5z-pp-optri': 0, 'aug-cc-pv5z-pp-rifit': 0, 'aug-cc-pv5z-pp': 0, 'aug-cc-pv5z-rifit': 1,
                'aug-cc-pv5z': 1, 'aug-cc-pv6z-rifit': 1, 'aug-cc-pv6z': 1, 'aug-cc-pv7z': 0, 'aug-cc-pvdz-dk': 0,
                'aug-cc-pvdz-dk3': 1, 'aug-cc-pvdz-optri': 0, 'aug-cc-pvdz-pp-optri': 0,
                'aug-cc-pvdz-pp-rifit': 0, 'aug-cc-pvdz-pp': 0, 'aug-cc-pvdz-rifit': 1, 'aug-cc-pvdz-x2c': 1,
                'aug-cc-pvdz': 1, 'aug-cc-pvqz-dk': 0, 'aug-cc-pvqz-dk3': 1, 'aug-cc-pvqz-optri': 0,
                'aug-cc-pvqz-pp-optri': 0, 'aug-cc-pvqz-pp-rifit': 0, 'aug-cc-pvqz-pp': 0, 'aug-cc-pvqz-rifit': 1,
                'aug-cc-pvqz-x2c': 1, 'aug-cc-pvqz': 1, 'aug-cc-pvtz-dk': 0, 'aug-cc-pvtz-dk3': 1,
                'aug-cc-pvtz-j': 0, 'aug-cc-pvtz-optri': 0, 'aug-cc-pvtz-pp-optri': 0, 'aug-cc-pvtz-pp-rifit': 0,
                'aug-cc-pvtz-pp': 0, 'aug-cc-pvtz-rifit': 1, 'aug-cc-pvtz-x2c': 1, 'aug-cc-pvtz': 1,
                'aug-cc-pwcv5z-dk': 0, 'aug-cc-pwcv5z-pp-optri': 0, 'aug-cc-pwcv5z-pp-rifit': 0,
                'aug-cc-pwcv5z-pp': 0, 'aug-cc-pwcv5z-rifit': 1, 'aug-cc-pwcv5z': 0, 'aug-cc-pwcvdz-dk3': 1,
                'aug-cc-pwcvdz-pp-optri': 0, 'aug-cc-pwcvdz-pp-rifit': 0, 'aug-cc-pwcvdz-pp': 0,
                'aug-cc-pwcvdz-rifit': 1, 'aug-cc-pwcvdz-x2c': 1, 'aug-cc-pwcvdz': 0, 'aug-cc-pwcvqz-dk': 0,
                'aug-cc-pwcvqz-dk3': 1, 'aug-cc-pwcvqz-pp-optri': 0, 'aug-cc-pwcvqz-pp-rifit': 0,
                'aug-cc-pwcvqz-pp': 0, 'aug-cc-pwcvqz-rifit': 1, 'aug-cc-pwcvqz-x2c': 1, 'aug-cc-pwcvqz': 0,
                'aug-cc-pwcvtz-dk': 0, 'aug-cc-pwcvtz-dk3': 1, 'aug-cc-pwcvtz-pp-optri': 0,
                'aug-cc-pwcvtz-pp-rifit': 0, 'aug-cc-pwcvtz-pp': 0, 'aug-cc-pwcvtz-rifit': 1,
                'aug-cc-pwcvtz-x2c': 1, 'aug-cc-pwcvtz': 0, 'aug-ccx-5z': 1, 'aug-ccx-dz': 1, 'aug-ccx-qz': 1,
                'aug-ccx-tz': 1, 'aug-mcc-pv5z': 0, 'aug-mcc-pv6z': 0, 'aug-mcc-pv7z': 0, 'aug-mcc-pv8z': 0,
                'aug-mcc-pvqz': 0, 'aug-mcc-pvtz': 0, 'aug-pc-0': 0, 'aug-pc-1': 0, 'aug-pc-2': 0, 'aug-pc-3': 0,
                'aug-pc-4': 0, 'aug-pch-1': 1, 'aug-pch-2': 1, 'aug-pch-3': 1, 'aug-pch-4': 1, 'aug-pcj-0': 1,
                'aug-pcj-0_2006': 0, 'aug-pcj-1': 1, 'aug-pcj-1_2006': 0, 'aug-pcj-2': 1, 'aug-pcj-2_2006': 0,
                'aug-pcj-3': 1, 'aug-pcj-3_2006': 0, 'aug-pcj-4': 1, 'aug-pcj-4_2006': 0, 'aug-pcs-0': 0,
                'aug-pcs-1': 0, 'aug-pcs-2': 0, 'aug-pcs-3': 0, 'aug-pcs-4': 0, 'aug-pcseg-0': 1,
                'aug-pcseg-1': 1, 'aug-pcseg-2': 1, 'aug-pcseg-3': 1, 'aug-pcseg-4': 1, 'aug-pcsseg-0': 1,
                'aug-pcsseg-1': 1, 'aug-pcsseg-2': 1, 'aug-pcsseg-3': 1, 'aug-pcsseg-4': 1, 'aug-pcx-1': 1,
                'aug-pcx-2': 1, 'aug-pcx-3': 1, 'aug-pcx-4': 1, 'aug-pv7z': 0, 'binning 641(d)': 0,
                'binning 641(df)': 0, 'binning 641+(d)': 0, 'binning 641+(df)': 0, 'binning 641+': 0,
                'binning 641': 0, 'binning 962(d)': 0, 'binning 962(df)': 0, 'binning 962+(d)': 0,
                'binning 962+(df)': 0, 'binning 962+': 0, 'binning 962': 0, 'cc-pcv5z': 0, 'cc-pcvdz-dk': 0,
                'cc-pcvdz-f12-optri': 0, 'cc-pcvdz-f12-rifit': 0, 'cc-pcvdz-f12': 0, 'cc-pcvdz': 0,
                'cc-pcvqz-dk': 0, 'cc-pcvqz-f12-optri': 0, 'cc-pcvqz-f12-rifit': 0, 'cc-pcvqz-f12': 0,
                'cc-pcvqz': 0, 'cc-pcvtz-dk': 0, 'cc-pcvtz-f12-optri': 0, 'cc-pcvtz-f12-rifit': 0,
                'cc-pcvtz-f12': 0, 'cc-pcvtz': 0, 'cc-pv(5+d)z': 1, 'cc-pv(d+d)z': 1, 'cc-pv(q+d)z': 1,
                'cc-pv(t+d)z': 1, 'cc-pv5z(fi/sf/fw)': 0, 'cc-pv5z(fi/sf/lc)': 0, 'cc-pv5z(fi/sf/sc)': 0,
                'cc-pv5z(pt/sf/fw)': 0, 'cc-pv5z(pt/sf/lc)': 0, 'cc-pv5z(pt/sf/sc)': 0, 'cc-pv5z-dk': 0,
                'cc-pv5z-f12(rev2)': 1, 'cc-pv5z-f12': 1, 'cc-pv5z-jkfit': 1, 'cc-pv5z-pp-rifit': 0,
                'cc-pv5z-pp': 0, 'cc-pv5z-rifit': 1, 'cc-pv5z': 1, 'cc-pv6z-rifit': 1, 'cc-pv6z': 1, 'cc-pv8z': 0,
                'cc-pv9z': 0, 'cc-pvdz(fi/sf/fw)': 0, 'cc-pvdz(fi/sf/lc)': 0, 'cc-pvdz(fi/sf/sc)': 0,
                'cc-pvdz(pt/sf/fw)': 0, 'cc-pvdz(pt/sf/lc)': 0, 'cc-pvdz(pt/sf/sc)': 0, 'cc-pvdz(seg-opt)': 0,
                'cc-pvdz-dk': 0, 'cc-pvdz-dk3': 1, 'cc-pvdz-f12(rev2)': 1, 'cc-pvdz-f12-optri': 0,
                'cc-pvdz-f12': 0, 'cc-pvdz-pp-rifit': 0, 'cc-pvdz-pp': 0, 'cc-pvdz-rifit': 1, 'cc-pvdz-x2c': 1,
                'cc-pvdz': 1, 'cc-pvqz(fi/sf/fw)': 0, 'cc-pvqz(fi/sf/lc)': 0, 'cc-pvqz(fi/sf/sc)': 0,
                'cc-pvqz(pt/sf/fw)': 0, 'cc-pvqz(pt/sf/lc)': 0, 'cc-pvqz(pt/sf/sc)': 0, 'cc-pvqz(seg-opt)': 0,
                'cc-pvqz-dk': 0, 'cc-pvqz-dk3': 1, 'cc-pvqz-f12(rev2)': 1, 'cc-pvqz-f12-optri': 0,
                'cc-pvqz-f12': 0, 'cc-pvqz-jkfit': 1, 'cc-pvqz-pp-rifit': 0, 'cc-pvqz-pp': 0, 'cc-pvqz-rifit': 1,
                'cc-pvqz-x2c': 1, 'cc-pvqz': 1, 'cc-pvtz(fi/sf/fw)': 0, 'cc-pvtz(fi/sf/lc)': 0,
                'cc-pvtz(fi/sf/sc)': 0, 'cc-pvtz(pt/sf/fw)': 0, 'cc-pvtz(pt/sf/lc)': 0, 'cc-pvtz(pt/sf/sc)': 0,
                'cc-pvtz(seg-opt)': 0, 'cc-pvtz-dk': 0, 'cc-pvtz-dk3': 1, 'cc-pvtz-f12(rev2)': 1,
                'cc-pvtz-f12-optri': 0, 'cc-pvtz-f12': 0, 'cc-pvtz-jkfit': 1, 'cc-pvtz-pp-rifit': 0,
                'cc-pvtz-pp': 0, 'cc-pvtz-rifit': 1, 'cc-pvtz-x2c': 1, 'cc-pvtz': 1, 'cc-pwcv5z-dk': 0,
                'cc-pwcv5z-pp-rifit': 0, 'cc-pwcv5z-pp': 0, 'cc-pwcv5z-rifit': 1, 'cc-pwcv5z': 0,
                'cc-pwcvdz-dk3': 1, 'cc-pwcvdz-pp-rifit': 0, 'cc-pwcvdz-pp': 0, 'cc-pwcvdz-rifit': 1,
                'cc-pwcvdz-x2c': 1, 'cc-pwcvdz': 0, 'cc-pwcvqz-dk': 0, 'cc-pwcvqz-dk3': 2,
                'cc-pwcvqz-pp-rifit': 0, 'cc-pwcvqz-pp': 0, 'cc-pwcvqz-rifit': 1, 'cc-pwcvqz-x2c': 1,
                'cc-pwcvqz': 0, 'cc-pwcvtz-dk': 0, 'cc-pwcvtz-dk3': 1, 'cc-pwcvtz-pp-rifit': 0, 'cc-pwcvtz-pp': 0,
                'cc-pwcvtz-rifit': 1, 'cc-pwcvtz-x2c': 1, 'cc-pwcvtz': 0, 'ccemd-2': 0, 'ccemd-3': 0,
                'ccj-pv5z': 0, 'ccj-pvdz': 0, 'ccj-pvqz': 0, 'ccj-pvtz': 0, 'ccx-5z': 1, 'ccx-dz': 1, 'ccx-qz': 1,
                'ccx-tz': 1, 'coemd-2': 0, 'coemd-3': 0, 'coemd-4': 0, 'coemd-ref': 0, 'cologne dkh2': 0,
                'crenbl ecp': 0, 'crenbl': 0, 'crenbs ecp': 0, 'crenbs': 0, 'd-aug-cc-pv5z': 0,
                'd-aug-cc-pv6z': 0, 'd-aug-cc-pvdz': 0, 'd-aug-cc-pvqz': 0, 'd-aug-cc-pvtz': 0, 'def2-ecp': 1,
                'def2-qzvp-rifit': 1, 'def2-qzvp': 1, 'def2-qzvpd': 1, 'def2-qzvpp-rifit': 1, 'def2-qzvpp': 1,
                'def2-qzvppd-rifit': 1, 'def2-qzvppd': 1, 'def2-sv(p)-jkfit': 1, 'def2-sv(p)-rifit': 1,
                'def2-sv(p)': 1, 'def2-svp-rifit': 1, 'def2-svp': 1, 'def2-svpd-rifit': 1, 'def2-svpd': 1,
                'def2-tzvp-rifit': 1, 'def2-tzvp': 1, 'def2-tzvpd-rifit': 1, 'def2-tzvpd': 1,
                'def2-tzvpp-rifit': 1, 'def2-tzvpp': 1, 'def2-tzvppd-rifit': 1, 'def2-tzvppd': 1,
                'def2-universal-jfit': 1, 'def2-universal-jkfit': 1, 'demon2k-dzvp-gga': 1, 'dfo+-nrlmol': 1,
                'dfo-1-bhs': 1, 'dfo-1': 1, 'dfo-2': 1, 'dfo-nrlmol': 1, 'dgauss-a1-dftjfit': 0,
                'dgauss-a1-dftxfit': 0, 'dgauss-a2-dftjfit': 0, 'dgauss-a2-dftxfit': 0, 'dgauss-dzvp': 0,
                'dgauss-dzvp2': 0, 'dgauss-tzvp': 0, 'dhf-ecp': 0, 'dhf-qzvp': 0, 'dhf-qzvpp': 0, 'dhf-sv(p)': 0,
                'dhf-svp': 0, 'dhf-tzvp': 0, 'dhf-tzvpp': 0, 'dz (dunning-hay)': 0,
                'dz + double rydberg (dunning-hay)': 0, 'dz + rydberg (dunning-hay)': 0, 'dzp (dunning-hay)': 0,
                'dzp + diffuse (dunning-hay)': 0, 'dzp + rydberg (dunning-hay)': 0, 'fano-5z': 1, 'fano-6z': 1,
                'fano-dz': 1, 'fano-qz': 1, 'fano-tz': 1, 'hgbs-5': 1, 'hgbs-7': 1, 'hgbs-9': 1, 'hgbsp1-5': 1,
                'hgbsp1-7': 1, 'hgbsp1-9': 1, 'hgbsp2-5': 1, 'hgbsp2-7': 1, 'hgbsp2-9': 1, 'hgbsp3-5': 1,
                'hgbsp3-7': 1, 'hgbsp3-9': 1, 'iglo-ii': 0, 'iglo-iii': 0, 'jgauss-dzp': 1, 'jgauss-qz2p': 1,
                'jgauss-qzp': 1, 'jgauss-tzp1': 1, 'jgauss-tzp2': 1, 'jorge-5zp-dkh': 1, 'jorge-5zp': 1,
                'jorge-6zp-dkh': 1, 'jorge-6zp': 1, 'jorge-a5zp': 1, 'jorge-adzp': 1, 'jorge-aqzp': 1,
                'jorge-atzp': 1, 'jorge-dzp-dkh': 1, 'jorge-dzp': 1, 'jorge-qzp-dkh': 1, 'jorge-qzp': 1,
                'jorge-tzp-dkh': 1, 'jorge-tzp': 1, 'jul-cc-pv(d+d)z': 0, 'jul-cc-pv(q+d)z': 0,
                'jul-cc-pv(t+d)z': 0, 'jun-cc-pv(d+d)z': 0, 'jun-cc-pv(q+d)z': 0, 'jun-cc-pv(t+d)z': 0,
                'koga unpolarized': 1, 'lanl08(d)': 0, 'lanl08(f)': 0, 'lanl08+': 0, 'lanl08': 0,
                'lanl2dz ecp': 0, 'lanl2dz': 0, 'lanl2dzdp': 0, 'lanl2tz(f)': 0, 'lanl2tz+': 0, 'lanl2tz': 0,
                'm6-31g': 0, 'm6-31g*': 0, 'maug-cc-pv(d+d)z': 0, 'maug-cc-pv(q+d)z': 0, 'maug-cc-pv(t+d)z': 0,
                'may-cc-pv(q+d)z': 0, 'may-cc-pv(t+d)z': 0, 'midi!': 1, 'midi': 0, 'midix': 1, 'mini': 0,
                'modified-lanl2dz': 0, 'nasa ames ano': 0, 'nasa ames ano2': 0, 'nasa ames cc-pcv5z': 0,
                'nasa ames cc-pcvqz': 0, 'nasa ames cc-pcvtz': 0, 'nasa ames cc-pv5z': 0, 'nasa ames cc-pvqz': 0,
                'nasa ames cc-pvtz': 0, 'nlo-v': 0, 'nmr-dkh (tz2p)': 0, 'orp': 1, 'partridge uncontracted 1': 0,
                'partridge uncontracted 2': 0, 'partridge uncontracted 3': 0, 'partridge uncontracted 4': 0,
                'pc-0': 0, 'pc-1': 0, 'pc-2': 0, 'pc-3': 0, 'pc-4': 0, 'pcemd-2': 0, 'pcemd-3': 0, 'pcemd-4': 0,
                'pch-1': 1, 'pch-2': 1, 'pch-3': 1, 'pch-4': 1, 'pcj-0': 1, 'pcj-0_2006': 0, 'pcj-1': 1,
                'pcj-1_2006': 0, 'pcj-2': 1, 'pcj-2_2006': 0, 'pcj-3': 1, 'pcj-3_2006': 0, 'pcj-4': 1,
                'pcj-4_2006': 0, 'pcs-0': 0, 'pcs-1': 0, 'pcs-2': 0, 'pcs-3': 0, 'pcs-4': 0, 'pcseg-0': 1,
                'pcseg-1': 1, 'pcseg-2': 1, 'pcseg-3': 1, 'pcseg-4': 1, 'pcsseg-0': 1, 'pcsseg-1': 1,
                'pcsseg-2': 1, 'pcsseg-3': 1, 'pcsseg-4': 1, 'pcx-1': 1, 'pcx-2': 1, 'pcx-3': 1, 'pcx-4': 1,
                'psbkjc': 0, 'pt - mdzp': 0, 'pv6z': 0, 'pv7z': 0, 'roos augmented double zeta ano': 0,
                'roos augmented triple zeta ano': 0, 's3-21g': 0, 's3-21g*': 0, 's6-31g': 0, 's6-31g*': 0,
                'sadlej pvtz': 1, 'sadlej+': 1, 'sap_grasp_large': 1, 'sap_grasp_small': 1, 'sap_helfem_large': 1,
                'sap_helfem_small': 1, 'sapporo-dkh3-dzp-2012-diffuse': 1, 'sapporo-dkh3-dzp-2012': 1,
                'sapporo-dkh3-dzp-diffuse': 1, 'sapporo-dkh3-dzp': 1, 'sapporo-dkh3-qzp-2012-diffuse': 1,
                'sapporo-dkh3-qzp-2012': 1, 'sapporo-dkh3-qzp-diffuse': 1, 'sapporo-dkh3-qzp': 1,
                'sapporo-dkh3-tzp-2012-diffuse': 1, 'sapporo-dkh3-tzp-2012': 1, 'sapporo-dkh3-tzp-diffuse': 1,
                'sapporo-dkh3-tzp': 1, 'sapporo-dzp-2012-diffuse': 1, 'sapporo-dzp-2012': 1,
                'sapporo-dzp-diffuse': 1, 'sapporo-dzp': 1, 'sapporo-qzp-2012-diffuse': 1, 'sapporo-qzp-2012': 1,
                'sapporo-qzp-diffuse': 1, 'sapporo-qzp': 1, 'sapporo-tzp-2012-diffuse': 1, 'sapporo-tzp-2012': 1,
                'sapporo-tzp-diffuse': 1, 'sapporo-tzp': 1, 'sarc-dkh2': 0, 'sarc-zora': 0,
                'sarc2-qzv-dkh2-jkfit': 0, 'sarc2-qzv-dkh2': 0, 'sarc2-qzv-zora-jkfit': 0, 'sarc2-qzv-zora': 0,
                'sarc2-qzvp-dkh2-jkfit': 0, 'sarc2-qzvp-dkh2': 0, 'sarc2-qzvp-zora-jkfit': 0,
                'sarc2-qzvp-zora': 0, 'sbkjc polarized (p,2d) - lfk': 0, 'sbkjc-ecp': 0, 'sbkjc-vdz': 0,
                'sbo4-dz(d)-3g': 1, 'sbo4-dz(d,p)-3g': 1, 'sbo4-sz-3g': 1, 'scaled mini': 0, 'sto-2g': 1,
                'sto-3g': 1, 'sto-3g*': 1, 'sto-4g': 1, 'sto-5g': 1, 'sto-6g': 1, 'stuttgart rlc ecp': 0,
                'stuttgart rlc': 0, 'stuttgart rsc 1997 ecp': 0, 'stuttgart rsc 1997': 0, 'stuttgart rsc ano': 0,
                'stuttgart rsc segmented + ecp': 0, 'sv (dunning-hay)': 0, 'sv + double rydberg (dunning-hay)': 0,
                'sv + rydberg (dunning-hay)': 0, 'svp (dunning-hay)': 0, 'svp + diffuse (dunning-hay)': 0,
                'svp + diffuse + rydberg (dunning-hay)': 0, 'svp + rydberg (dunning-hay)': 0,
                'tz (dunning-hay)': 0, 'tzp-zora': 1, 'ugbs': 0, 'un-ccemd-ref': 0, 'un-pcemd-ref': 0,
                'wachters+f': 0, 'wtbs': 0, 'x2c-jfit-universal': 1, 'x2c-jfit': 1, 'x2c-qzvpall-2c-s': 1,
                'x2c-qzvpall-2c': 1, 'x2c-qzvpall-s': 1, 'x2c-qzvpall': 1, 'x2c-qzvppall-2c-s': 1,
                'x2c-qzvppall-2c': 1, 'x2c-qzvppall-s': 1, 'x2c-qzvppall': 1, 'x2c-sv(p)all-2c': 0,
                'x2c-sv(p)all-s': 1, 'x2c-sv(p)all': 0, 'x2c-svpall-2c': 0, 'x2c-svpall-s': 1, 'x2c-svpall': 0,
                'x2c-tzvpall-2c': 0, 'x2c-tzvpall-s': 1, 'x2c-tzvpall': 0, 'x2c-tzvppall-2c': 0,
                'x2c-tzvppall-s': 1, 'x2c-tzvppall': 0}


def getName(getter) -> str:
    """
    :param getter: either the symbol or the atomic number of an atom (case insensitive)
    :return: the full name of the atom (lower case)
    """
    if type(getter) == str:
        getter = getter.lower()
    if getter in SYMBOLS:
        return NAMES[SYMBOLS.index(getter)]
    elif getter in NUMBERS:
        return NAMES[NUMBERS.index(getter)]


def getSymbol(getter) -> str:
    """
    :param getter: either the full name or the atomic number of an atom (case insensitive)
    :return: the symbol of the atom (lower case)
    """
    if type(getter) == str:
        getter = getter.lower()
    if getter in NAMES:
        return SYMBOLS[NAMES.index(getter)]
    elif getter in NUMBERS:
        return SYMBOLS[NUMBERS.index(getter)]


def getNumber(getter) -> int:
    """
    :param getter: either the full name or the symbol of an atom (case insensitive)
    :return: the atomic number of the atom
    """
    if type(getter) == str:
        getter = getter.lower()
    if getter in SYMBOLS:
        return NUMBERS[SYMBOLS.index(getter)]
    elif getter in NAMES:
        return NUMBERS[NAMES.index(getter)]


def getMass(getter) -> float:
    """
    :param getter:either the full name or the symbol or the atomic number of an atom (case insensitive)
    :return: the atomic mass of the atom
    """
    if type(getter) == str:
        getter = getter.lower()
    if getter in SYMBOLS:
        return MASS[SYMBOLS.index(getter)]
    elif getter in NAMES:
        return MASS[NAMES.index(getter)]
    elif getter in NUMBERS:
        return MASS[NUMBERS.index(getter)]
