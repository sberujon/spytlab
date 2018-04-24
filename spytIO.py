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
    filename=str(filename)
    if filename.endswith('.edf'):
        im = edf.EdfFile(filename, access='rb')
        imarray = im.GetData(0)
    else :
        imarray = Image.open(filename)
        imarray = np.array(imarray)

    return imarray


def openSeq(filenames):
    if len(filenames) >0 :
        data=openImage(str(filenames[0]))
        height,width=data.shape
        toReturn = np.zeros((len(filenames), height, width),dtype=np.float32)
        i=0
        for file in filenames:
            data=openImage(str(file))
            toReturn[i,:,:]=data
            i+=1
        return toReturn
    raise Exception('spytlabIOError')


def makeDarkMean(Darkfiedls):


    nbslices, height, width = Darkfiedls.shape
    meanSlice = np.mean(Darkfiedls, axis=0)
    print ('-----------------------  mean Dark calculation done ------------------------- ')
    OutputFileName = '/Users/helene/PycharmProjects/spytlab/meanDarkTest.edf'
    outputEdf = edf.EdfFile(OutputFileName, access='wb+')
    outputEdf.WriteImage({}, meanSlice)
    return meanSlice


def saveEdf(data,filename):
    print(filename)
    dataToStore=np.asarray(data,np.float32)
    outputEdf = edf.EdfFile( filename, access='wb+')
    outputEdf.WriteImage({},dataToStore)


def save3D_Edf(data,filename):
    nbslices,height,width=data.shape
    for i in range(nbslices):
        textSlice='%4.4d'%i
        dataToSave=data[i,:,:]
        filenameSlice=filename+textSlice+'.edf'
        saveEdf(dataToSave,filenameSlice)



def savePNG(data,filename,min=0,max=0):
    if min == max:
        min=np.amin(data)
        max= np.amax(data)
    data16bit=data-min/(max-min)
    data16bit=np.asarray(data16bit,dtype=np.uint16)

    scipy.misc.imsave(filename,data16bit)



if __name__ == "__main__":

    # filename='ref1-1.edf'
    # filenames=glob.glob('*.edf')
    # data=openImage(filename)
    # savePNG(data,'ref.png',100,450)
    # print( data.shape)
    #
    #
    # rootfolder = '/Volumes/VISITOR/md1097/id17/Phantoms/TwoDimensionalPhantom/GrilleFils/Absorption52keV/'
    # referencesFilenames = glob.glob(rootfolder + 'Projref/*.edf')
    # sampleFilenames = glob.glob(rootfolder + 'Proj/*.edf')
    # referencesFilenames.sort()
    # sampleFilenames.sort()
    # print(' lalalal ')
    # print (referencesFilenames)
    # print (sampleFilenames)

    rootfolder = '/Volumes/ID17/broncho/IHR_April2018/darkField_copy/'
    DarkFilenames = glob.glob(rootfolder + '*.edf')
    DarkFilenames.sort()
    print DarkFilenames

    DarkFiles = openSeq(DarkFilenames)
    print  ('lalala')

    makeDarkMean(DarkFiles,outputDarkmean)

