import numpy as np
import EdfFile as edf

import glob
from numpy.fft import fftshift as fftshift
from numpy.fft import ifftshift as ifftshift
from numpy.fft import fft2 as fft2
from numpy.fft import ifft2 as ifft2
import frankoChellappa as fc
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


def zncc(img1, img2, w):
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
def found_max(Im,max=-1000)
 # find max value in the  cc map
   Im=ccmap
    for i in range  (1,windowSize-1,1):
        for j in range  (1,windowSize-1,1):
            if (windowSize*i+j)> max :
                max=windowSize*i+j
            return max

def calculateDisplacment(Ir,Is,window=1,step=1):
    dI = (Is - Ir * (np.mean(Is) / np.mean(Ir)))
    windowSize=window*2+1
    nbslices, DimY, DimX = Im.shape
    values = []
    #size of the ouput image will be reduced by the size of the interrogation window (no info on the edge)
    ImOut=np.zeros((nbslices,DimY-windowSize, DimX-windowSize))
    # window size crop:
    cropIr=Ir[:,i-window:i+window, j-window:j+window]
    cropIs=Is[:,i-window:i+window, j-window:j+window]

    # look through all the pixel positions
    for oi in range (windowSize+1, DimY-windowSize,1):
        for oj in  range (windowSize+1, DimY-windowSize,1):

            # look on the neighbour pixels of the reference stack
            for j in  range (j-window:j+windowSize):
               for i in range (i - window: i + windowSize):

                # look for the third dimension
                    for k in enumerate (nbslices):
                    #calculation of the peak of correlaction with ZNCC
#                         # ....... ie faire  zncc(Ir,Is,)

                      return ccMap
                    #and found_max in ccmap.........
                    # calculation of dx, dy, de, transmission, fidelity
                  #  dx=displacmentX[]
                  #  dy=displacmentY[]
                #
                 #   phi = fc.frankotchellappa(dx, dy, False)
        #            T= Is-phi
        #            fidelity=  ccmap

    return {'T': transmission, 'dx': dx, 'dy': dy, 'df': df , 'fidelity': fidelity}



if __name__ == "__main__":
    print ' Optical Flow Tomo '
    print 'Test One File'
    Ir=spytIO.openImage('ref1-1.edf')
    Is= spytIO.openImage('samp1-1.edf')

