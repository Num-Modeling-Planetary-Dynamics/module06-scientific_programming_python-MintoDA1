import numpy as np
import glob
import os

def load():
    datadir = os.path.join(os.pardir,"data")

    # Initialize the two empty lists we plan to return
    planet_names = []
    xv_data = []

    # Extract the names of all the input files contained in the data directory
    datafiles = glob.glob(os.path.join(datadir, "*-XV.csv"))

    # Iterate over the names of the files in the list
    for filename in datafiles:
        planet_names.append(filename.split(os.path.sep)[-1].split('-')[0])  # Extract the name of the planet from the name of the file
        data = np.genfromtxt(filename, delimiter=',', names=True,dtype=np.float64)
        data = np.array([np.array(list(d)) for d in data])
        xv_data.append(data)


    return dict(zip(planet_names,xv_data))

if __name__ == '__main__':
    xv_data = load()