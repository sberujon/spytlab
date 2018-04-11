import spytIO
import glob
import os
from numpy.fft import fftshift as fftshift
from numpy.fft import ifftshift as ifftshift
from numpy.fft import fft2 as fft2
from numpy.fft import ifft2 as ifft2

from math import pi as pi
from math import floor as floor

import frankoChellappa as fc

import numpy as np
import corrections as corr
import fastTomoExperiment as esrfTomo





def derivativesByOpticalflow(intensityImage,derivative,alpha=0,sig_scale=0):

    Nx, Ny = derivative.shape
    # fourier transfomm of the derivative and shift low frequencies to the centre
    ftdI = fftshift(fft2(derivative))
    # calculate frequencies
    dqx = 2 * pi / (Nx)
    dqy = 2 * pi / (Ny)
    Qx, Qy = np.meshgrid((np.arange(0, Ny) - floor(Ny / 2) - 1) * dqy, (np.arange(0, Nx) - floor(Nx / 2) - 1) * dqx)


    #building filters


    sigmaX = dqx / 1. * np.power(sig_scale,2)
    sigmaY = dqy / 1. * np.power(sig_scale,2)
    #sigmaX=sig_scale
    #sigmaY = sig_scale

    g = np.exp(-(((Qx)**2) / 2. / sigmaX + ((Qy)**2) / 2. / sigmaY))
    #g = np.exp(-(((np.power(Qx, 2)) / 2) / sigmaX + ((np.power(Qy, 2)) / 2) / sigmaY))
    beta = 1 - g;

    i = complex(0, 1)
    # fourier filters
    ftfiltX = (i * Qx / ((Qx**2 + Qy**2 + alpha))*beta)
    #ftfiltX = (1 * i * Qx / (np.power(Qx, 2) + np.power(Qy, 2) + alpha) * beta)
    ftfiltX[np.isnan(ftfiltX)] = 0

    ftfiltY = (i* Qy/ ((Qx**2 + Qy**2 + alpha))*beta)
    #ftfiltY = (1 * i * Qy / (np.power(Qx, 2) + np.power(Qy, 2) + alpha) * beta)
    ftfiltY[np.isnan(ftfiltY)] = 0

    # output calculation
    dImX = 1. / intensityImage * ifft2(ifftshift(ftfiltX * ftdI))
    dImY = 1. / intensityImage * ifft2(ifftshift(ftfiltY * ftdI))

    return dImX.real,dImY.real





def kottler(dX,dY):
    print 'kottler'
    i = complex(0, 1)
    Nx, Ny = dX.shape
    dqx = 2 * pi / (Nx)
    dqy = 2 * pi / (Ny)
    Qx, Qy = np.meshgrid((np.arange(0, Ny) - floor(Ny / 2) - 1) * dqy, (np.arange(0, Nx) - floor(Nx / 2) - 1) * dqx)

    polarAngle = np.arctan2(Qy, Qx)
    ftphi = fftshift(fft2(dX + i * dY))*np.exp(i*polarAngle)
    ftphi[np.isnan(ftphi)] = 0
    phi3 = ifft2(fftshift(ftphi))
    return phi3



def LarkinAnissonSheppard(dx,dy,alpha =0 ,sigma=0):
    Nx, Ny = dx.shape
    i = complex(0, 1)
    G= dx + i*dy
    # fourier transfomm of the G function
    fourrierOfG = fftshift(fft2(G))


    dqx = 2 * pi / (Nx)
    dqy = 2 * pi / (Ny)
    Qx, Qy = np.meshgrid((np.arange(0, Ny) - floor(Ny / 2) - 1) * dqy, (np.arange(0, Nx) - floor(Nx / 2) - 1) * dqx)

    ftfilt = 1 / (i*Qx - Qy)
    ftfilt[np.isnan(ftfilt)] = 0
    phi=ifft2(ifftshift(ftfilt*fourrierOfG))
    phi=np.absolute(phi.real)
    return phi


def parseESRFTomoFolder(folderpath,outputFolder):
    print 'ESRFTomoFolder'
    scanName=os.path.basename(folderpath)
    parametersScanFilename=folderpath+'/'+scanName+'.xml'
    print parametersScanFilename
    tomoExperiment=esrfTomo.FastTomoExperiment(parametersScanFilename,outputFolder)
    print 'numberFlatField: '
    print tomoExperiment.numberFlatField
    tomoExperiment.createAverageWfandDf()
    tomoExperiment.findCenterOfRotation()
    print 'Cor Found at '+str(tomoExperiment.cor)
    projectionsFileNames=tomoExperiment.getProjectionsName()
    darkFieldFilename=tomoExperiment.darkOutputFile
    referenceFileNames= tomoExperiment.getReferencesFileNames()

    print referenceFileNames








if __name__ == "__main__":
    inputFolder='/Volumes/ID17/speckle/md1097/id17/Phantoms/ThreeDimensionalPhantom/Speckle_Foam1_52keV_6um_xss_bis_012_'
    outputFolder='/Volumes/ID17/speckle/md1097/id17/Phantoms/ThreeDimensionalPhantom/OpticalFlow'
    parseESRFTomoFolder(inputFolder,outputFolder)


    print ' Optical Flow Tomo '
    print 'Test One File'
    Ir=spytIO.openImage('ref1-1.edf')
    Is= spytIO.openImage('samp1-1.edf')
    #offsett=corr.registerRefAndSample(Ir,Is,1000)
    #print offsett


    sigma=0.9
    alpha=0

    dI = (Is - Ir* (np.mean(Is)/np.mean(Ir)))
    dx, dy = derivativesByOpticalflow(Ir, dI, alpha=alpha, sig_scale=sigma)
    phi = fc.frankotchellappa(dx, dy, False)
    phi3=kottler(dx,dy)

    phi2=LarkinAnissonSheppard(dx,dy)

    spytIO.saveEdf(dx.real,'output/dx.edf')
    spytIO.saveEdf(dy.real, 'output/dy.edf')
    spytIO.saveEdf(phi.real, 'output/phi.edf')
    spytIO.saveEdf(phi2.real, 'output/phi2.edf')
    spytIO.saveEdf(phi3.real, 'output/phi3.edf')


# open images



