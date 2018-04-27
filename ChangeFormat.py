import os
import glob
import spytIO
import numpy as np
import utils

if __name__ == "__main__":
    inputFolder='/Volumes/ID17/speckle/md1097/id17/Phantoms/ThreeDimensionalPhantom/OpticalFlow/dy/'
    outputFolder='/Volumes/ID17/speckle/md1097/id17/Phantoms/ThreeDimensionalPhantom/OpticalFlow/dy_32/'
    utils.spytMkDir(outputFolder)
    files=glob.glob(inputFolder+'/*.edf')

    files.sort()
    for filename in files:
        print(filename)
        data=spytIO.openImage(filename)
        data=np.asarray(data,np.float32)
        outputFilename=outputFolder+'/'+os.path.basename(filename)
        print(outputFilename)
        spytIO.saveEdf(data,outputFilename)
