from astropy.io import fits

with fits.open('hw2/output.fits') as hdul:
    print(hdul.info())
    header = hdul[0].header
    data = hdul[0].data
print(header.cards)
print(data)