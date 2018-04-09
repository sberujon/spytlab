import numpy as np
import EdfFile as edf

import glob
from numpy.fft import fftshift as fftshift
from numpy.fft import ifftshift as ifftshift
from numpy.fft import fft2 as fft2
from numpy.fft import ifft2 as ifft2

from math import pi as pi
from math import floor as floor

import frankoChellappa as fc
from ioImage import openImage as openImage


def zncc(Ir,Is):
    # Calculate a characteristic form images called ZNCC (Zero-Normalized Cross Correlation)
    meanIr = np.mean(Ir)
    stdIr = np.std(Ir)
    meanIs = np.mean(Is)
    stdIs = np.std(Is)



def calculateDisplacment(Ir,Is,window=1,step=1):
    dI = (Is - Ir * (np.mean(Is) / np.mean(Ir)))
    windowSize=window*2+1
    DimX, DimY = dI.shape

    # look through all the pixel positions
    for i in enumerate (DimY):
        for j in enumerate(DimX):




    return {'T': transmission, 'dx': dx, 'dy': dy, 'df': df }



if __name__ == "__main__":
    print ' Optical Flow Tomo '
    print 'Test One File'
    Ir=spytIO.openImage('ref1-1.edf')
    Is= spytIO.openImage('samp1-1.edf')

