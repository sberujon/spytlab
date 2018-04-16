import numpy as np
import corrections as corr
import fastTomoExperiment as esrfTomo
import OpticalFlow
import spytlabQT as qt
import glob
import os
import spytIO




def processOneProjection(listOfDictionnaries,projectionNumber):
    print('------------------------------------------------------')
    print('processOneProjection')
    projectionFiles=[]
    referencesFiles=[]
    darkFieldFiles=[]
    for dict in listOfDictionnaries :
        projectionFiles.append(dict['projections'][projectionNumber])
        referencesFiles.append(dict['references'][0])
        darkFieldFiles.append(dict['darkField'])
    print(projectionFiles)
    toReturn=OpticalFlow.processProjectionSetWithDarkFields(projectionFiles,referencesFiles,darkFieldFiles)
    return toReturn




def createFolder(folder):
    if not (os.path.exists(folder)):
        os.mkdir(folder)

def processAllFolders(listOfFolders,outputFolder):
    dxFolder = outputFolder + '/dx/'
    dyFolder = outputFolder + '/dy/'
    phiFolder = outputFolder + '/phi/'
    phi2Folder = outputFolder + '/phi2/'
    phi3Folder = outputFolder + '/phi3/'
    createFolder(dxFolder)
    createFolder(dyFolder)
    createFolder(phiFolder)
    createFolder(phi2Folder)
    createFolder(phi3Folder)


    listOfDictionaries=[]
    for folder in listOfFolders:
        ddict=parseTomoFolderAndCreateRefFiles(folder)
        listOfDictionaries.append(ddict)

    numberOfProjections=len(listOfDictionaries[0]['projections'])
    for projectionNumber in range (0,numberOfProjections):
        projectionNumber=4
        result=processOneProjection(listOfDictionaries,projectionNumber)
        textProj='%4.4d'%projectionNumber

        dx = result['dx']
        dy = result['dy']
        phi = result['phi']
        phi2 = result['phi2']
        phi3 = result['phi3']
        spytIO.saveEdf(dx, dxFolder + '/dx'+textProj+'.edf')
        spytIO.saveEdf(dy.real, dyFolder + '/dy'+textProj+'.edf')
        spytIO.saveEdf(phi.real, phiFolder + '/phi'+textProj+'.edf')
        spytIO.saveEdf(phi2.real, phi2Folder + '/phi2'+textProj+'.edf')
        spytIO.saveEdf(phi3.real, phi3Folder + '/phi3'+textProj+'.edf')






def parseTomoFolderAndCreateRefFiles(folderpath):
    scanName=os.path.basename(folderpath)
    parametersScanFilename=folderpath+'/'+scanName+'.xml'
    print(parametersScanFilename)
    tomoExperiment=esrfTomo.FastTomoExperiment(parametersScanFilename)
    print('numberFlatField: ')
    print(tomoExperiment.numberFlatField)

    #tomoExperiment.createAverageWfandDf()
    #tomoExperiment.findCenterOfRotation()
    print('Cor Found at '+str(tomoExperiment.cor))
    projectionsFileNames=tomoExperiment.getProjectionsName()
    projectionsFileNames.sort()
    darkFieldFilename='Bidon'#tomoExperiment.darkOutputFile
    referenceFileNames= tomoExperiment.getReferencesFileNames()
    referenceFileNames.sort()
    print(referenceFileNames)
    ddict={}
    ddict['tomoFileName']=parametersScanFilename
    ddict['projections']=projectionsFileNames
    ddict['references']=referenceFileNames
    ddict['darkField']=darkFieldFilename
    ddict['COR'] = tomoExperiment.cor
    return ddict



if __name__ == "__main__":
    inputFolder='/Volumes/ID17/speckle/md1097/id17/Phantoms/ThreeDimensionalPhantom/'
    tomoFolders=glob.glob(inputFolder+'Speckle_Foam1_52keV_6um_xss_bis*')
    tomoFolders.sort()
    processAllFolders(tomoFolders)

    #result=parseTomoFolderAndCreateRefFiles(tomoFolders[0])
    #print result


