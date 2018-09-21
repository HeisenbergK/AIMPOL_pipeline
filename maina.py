from astropy.table import Table
from astropy.io import fits, ascii
import matplotlib.pyplot as plt
from zscale import *
from pylab import annotate
import os
import sys

fold = sys.argv[1]
fold = str(fold)

os.chdir(fold)

filename = 'images.cat'
filer = open(filename)
cont = []
for line in filer:
    cont.append(line.strip('\n'))
contnew = []
for entry in cont:
    contnew.append(entry + '.mag.1')

chars = ('image', 'Flux1', 'Flux2', 'NormFlux', 'Sum1', 'Sum2', 'Aper1', 'Aper2', 'SArea1', 'Sarea2')
types = (object, float, float, float, float, float, float, float, float, float)
masterstartable = Table(names=chars, dtype=types)
userpsf = 5

for i in range(0, len(contnew)):
    imagename = cont[i]
    image = imagename.strip('_extr.fit')
    magname = contnew[i]
    imagehdu = fits.open(imagename)
    readdata = imagehdu[0].data
    readhead = imagehdu[0].header
    phot_results = ascii.read(magname)
    phot_results.rename_column("ID", 'id')
    phot_results.rename_column("XCENTER", 'x_fit')
    phot_results.rename_column("YCENTER", 'y_fit')
    phot_results.rename_column("FLUX", 'flux_fit')
    phot_results.rename_column("AREA", 'aper')
    phot_results.rename_column("SUM", 'sum')
    phot_results.rename_column("NSKY", 'sarea')
    newtable = phot_results['id', 'x_fit', 'y_fit', 'flux_fit', 'aper', 'sum', 'sarea']
    print(newtable)
    print("Please inspect the image for the standard star")
    plt.clf()
    todisp = readdata
    zmin, zmax = zscale_range(todisp)
    plt.imshow(todisp, cmap='gray', aspect=1, origin='lower', vmin=zmin, vmax=zmax)
    for entry in range(0, len(newtable['id'])):
        xpos = newtable['x_fit'][entry]
        ypos = newtable['y_fit'][entry]
        fluxin = newtable['flux_fit'][entry]
        num = entry + 1
        print("%s %s %s %s" % (str(num), str(xpos), str(ypos), str(fluxin)))
        annotate(str(num), xy=(xpos, ypos), xytext=(xpos + 0, ypos + userpsf), fontsize=3 * userpsf, xycoords='data',
                 color='green')
    plt.show()
    num = 1
    while True:
        num = raw_input("Enter the id of the 1st ray of the standard star:\t")
        try:
            num = int(num)
            break
        except ValueError:
            print("Try again")
    entry = num - 1
    ident1 = int(1)
    flux1 = float(newtable["flux_fit"][entry])
    xpos1 = float(newtable["x_fit"][entry])
    ypos1 = float(newtable["y_fit"][entry])
    s1 = float(newtable['sum'][entry])
    aper1 = float(newtable['aper'][entry])
    sarea1 = float(newtable['sarea'][entry])
    num = 1
    while True:
        num = raw_input("Enter the id of the 2nd ray of the standard star:\t")
        try:
            num = int(num)
            break
        except ValueError:
            print("Try again")
    entry = num - 1
    ident2 = int(2)
    flux2 = float(newtable["flux_fit"][entry])
    xpos2 = float(newtable["x_fit"][entry])
    ypos2 = float(newtable["y_fit"][entry])
    s2 = float(newtable['sum'][entry])
    aper2 = float(newtable['aper'][entry])
    sarea2 = float(newtable['sarea'][entry])

    normflux = (flux1-flux2)/(flux1+flux2)

    image = str(image)
    print image
    toap = [image, flux1, flux2, normflux, s1, s2, aper1, aper2, sarea1, sarea2]
    masterstartable.add_row(toap)

ascii.write(masterstartable, 'catalog.ecsv', format='ecsv')
