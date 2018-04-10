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

'''def get_average(img, u, v, n):
    """img as a square matrix of numbers"""
    s = 0
    for i in range(-n, n+1):
        for j in range(-n, n+1):
            s += img[u+i][v+j]
    return float(s)/(2*n+1)**2'''


def zncc(img1, img2, u1, v1, u2, v2, n):
    # Calculate  ZNCC (Zero-Normalized Cross Correlation) value between 2 images
    # calculate mean and std before


    std_deviation1 = get_standard_deviation(img1, u1, v1, n)
    std_deviation2 = get_standard_deviation(img2, u2, v2, n)
    avg1 = get_average(img1, u1, v1, n)
    avg2 = get_average(img2, u2, v2, n)

    s = 0
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
             s += (img1[u1 + i][v1 + j] - avg1) * (img2[u2 + i][v2 + j] - avg2)
    return float(s) / ((2 * n + 1) ** 2 * std_deviation1 * std_deviation2)

'''def get_standard_deviation(img, u, v, n):
    s = 0
    avg = get_average(img, u, v, n)
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            s += (img[u + i][v + j] - avg) ** 2
    return (s ** 0.5) / (2 * n + 1)'''


def calculateDisplacment(Ir,Is,window=1,step=1):
    dI = (Is - Ir * (np.mean(Is) / np.mean(Ir)))
    windowSize=window*2+1
    DimX, DimY = dI.shape
    values = []

    # look through all the pixel positions
    for i in enumerate (DimY):
        for j in enumerate(DimX):
            values.append()
            displacementX[x + y * DimX] =  bestccX.float
            displacementY[x + y * DimY] =  bestccY.float


    return {'T': transmission, 'dx': dx, 'dy': dy, 'df': df }



if __name__ == "__main__":
    print ' Optical Flow Tomo '
    print 'Test One File'
    Ir=spytIO.openImage('ref1-1.edf')
    Is= spytIO.openImage('samp1-1.edf')

