import os
mainfold = '/home/heisenbergk/Documents/PASIPHAE/Standards/ARIES/27nov/27-11-17'
stars = ['275', '276', '1965', '1969', '4776', '5118', '5137', 'bd59', 'hd14']

for star in stars:
    fold = mainfold+'/'+star+'/'+star+'/'+'FinalImages'
    fold = str(fold)
    os.system('python maina.py '+fold)
