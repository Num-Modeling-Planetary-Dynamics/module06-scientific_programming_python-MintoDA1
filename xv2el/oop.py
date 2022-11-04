import numpy as np
import os
import glob
import astropy.constants as const

class Orbits():

    def __init__(self, units="AUDAY"):

        self.set_unit_system(units)
        self.datadir = os.path.join(os.pardir, "data")

        return

    def set_unit_system(self,system):
        """
        Setter for setting the unit conversion between one of the standard sets.

        Parameters
        ----------
        system  : str - default = "AUDAY"
           One of the following:
           "SI"    : kg-m-s
           "CGS"   : g-cm-s
           "AUDAY" : Msun-AU-day
           "AUYR"  : Msun-AU-yr

        Returns
        ----------
        Sets the values of MU2KG, DU2M, and TU2S to the appropriate units:
        """

        # Define some global constants in SI units
        AU2M = const.au.value
        GMSunSI = const.GM_sun.value
        MSun = const.M_sun.value
        JD2S = 86400
        YR2S = np.double(365.25 * JD2S)

        if system == "AUDAY":
            self.MU2KG = MSun
            self.DU2M  = AU2M
            self.TU2S  = JD2S
        elif system == "AUYR" :
            self.MU2KG = MSun
            self.DU2M  = AU2M
            self.TU2S  = YR2S
        else:
            raise ValueError(f"{system} is an unknown unit system. Setting to SI")

        self.GMSun = GMSunSI * self.TU2S**2 / self.DU2M**3
        self.unit_system = system

        print(f"Set unit system to {system}")

        return

    def load_cartesian_data(self):
        """

        Parameters
        ----------
        name : str
            Name of planet

        Returns
        -------
            Sets the tvals, rvec, and vvec array instances and returns a helpful text message

        """

        # Initialize the two empty lists we plan to return
        planet_names = []
        xv_data = []

        # Extract the names of all the input files contained in the data directory
        datafiles = glob.glob(os.path.join(self.datadir, "*-XV.csv"))
        datafiles.sort()

        # Iterate over the names of the files in the list
        for filename in datafiles:
            planet_names.append(filename.split(os.path.sep)[-1].split('-')[
                                    0])  # Extract the name of the planet from the name of the file
            data = np.genfromtxt(filename, delimiter=',', names=True, dtype=np.float64)
            data = np.array([np.array(list(d)) for d in data])
            xv_data.append(data)
            print(f"Loaded cartesian vector data for {planet_names[-1]}")

        self.xv_data = dict(zip(planet_names, xv_data))
        return


if __name__ == '__main__':
    solar_system = Orbits()
    solar_system.load_cartesian_data()