# -*- coding: utf-8 -*-
"""
SpytLab speckle python lab
Author: Helene Labriet & Emmanuel Brun
Date: April 2018
"""

import EdfFile as edf
from PIL import Image
import numpy as np
import scipy
from scipy.misc import imsave as imsave
import glob

def openImage(filename):
    if filename.endswith('.edf'):
        im = edf.EdfFile(filename, access='rb')
        imarray = im.GetData(0)
    else :
        imarray = Image.open(filename)
        imarray = np.array(imarray)

    return imarray


def openSeq(filenames):
    if len(filenames) >0 :
        data=openImage(filenames[0])
        height,width=data.shape
        toReturn = np.zeros((len(filenames), height, width))
        i=0
        for file in filenames:
            data=openImage(file)
            toReturn[i,:,:]=data
            i+=1
        return toReturn
    raise Exception('spytlabIOError')


def saveEdf(data,filename):

    outputEdf = edf.EdfFile( filename+'.edf', access='wb+')
    outputEdf.WriteImage(data, filename)


def savePNG(data,filename,min=0,max=0):
    if min == max:
        min=np.amin(data)
        max= np.amax(data)
    data16bit=data-min/(max-min)
    data16bit=np.asarray(data16bit,dtype=np.uint16)

    scipy.misc.imsave(filename,data16bit)



if __name__ == "__main__":

    filename='ref1-1.edf'
    filenames=glob.glob('*.edf')
    data=openImage(filename)
    savePNG(data,'ref.png',100,450)
    print data.shape


    rootfolder = '/Volumes/VISITOR/md1097/id17/Phantoms/TwoDimensionalPhantom/GrilleFils/Absorption52keV/'
    referencesFilenames = glob.glob(rootfolder + 'Projref/*.edf')
    sampleFilenames = glob.glob(rootfolder + 'Proj/*.edf')
    referencesFilenames.sort()
    sampleFilenames.sort()
    print referencesFilenames
    print sampleFilenames

    Ir = openSeq(referencesFilenames)

    Is = openSeq(sampleFilenames)

    dI = (Is - Ir)