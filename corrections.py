from skimage.feature import register_translation
from scipy.ndimage import fourier_shift
import numpy as np
import spytIO
import EdfFile as edf




def registerRefAndSample(Ir,Is,precision):

    # correction of beam movementn
    shifts, error, phasediff = register_translation(Is, Ir, precision)
    offset_image = fourier_shift(np.fft.fftn(Ir), shifts)
    offset_image = np.fft.ifftn(offset_image)
    print (' the register correction shift is ( in pixels ) : ')
    print (shifts)
    print (' ----------------------- registration correction done------------------------ ')
    return offset_image.real

def errorDetection (Ir, Is):
    # correction of failed acquired  couple Ir and Is
    # Ir and Is are 3D array as [nbpoint,height,width] because openSeq return toReturn = np.zeros((len(filenames), height, width))
    nbPoints,height,width=Ir.shape
    print(len(nbPoints))
    pointsToDelete=[]
    for coupleOfPopints in range (0,nbPoints):
        sample=Is[coupleOfPopints,:,:]
        reference = Ir[coupleOfPopints, :, :]
        shifts, error, phasediff = registerRefAndSample(reference,sample, 1000)
        if shifts[0]> 10 or shifts [1] >10:
            pointsToDelete.append(coupleOfPopints)
            print('ERROR couple : deletion in progress ')

    if (len(pointsToDelete)>0):
        Ir=np.delete(Ir, pointsToDelete,axis=0)
        Is = np.delete(Is, pointsToDelete, axis=0)

    return Ir,Is



    print(' ----------------------- error detection correction done------------------------ ')


def normalization (Im, darkfield):
    # correction by flat or dark field
    #calculate mean and std of the image to be able to normalize
    nbslices, height, width = Im.shape
    print (len(nbslices))
    slicesNormalized = []
    meanSlice = np.mean(Im, axis=0)
    stdSlice = np.std(Im, axis=0)

    for slice in range(0, nbslices):
        ImCorrected=(Im[slice,:,:]-meanSlice[slice])/stdSlice[slice]

        ImCorrected=ImCorrected-darkfield
        slicesNormalized.append(ImCorrected)

    print ('-----------------------  normalization correction done ----------------------- ')
    return slicesNormalized






def normalizationMultipleDarkField (Im, darkfield):
    # correction by flat or dark field
    #calculate mean and std of the image to be able to normalize
    nbslices, height, width = Im.shape
    print (len(nbslices))
    slicesNormalized = []
    meanSlice = np.mean(Im, axis=0)
    stdSlice = np.std(Im, axis=0)

    for slice in range(0, nbslices):
        ImCorrected=(Im[slice,:,:]-meanSlice[slice])/stdSlice[slice]

        ImCorrected=ImCorrected-darkfield[slice]
        slicesNormalized.append(ImCorrected)

    print ('-----------------------  normalization correction done ----------------------- ')
    return slicesNormalized




def normalization2D (Im, darkfield):
    # correction by flat or dark field
    #calculate mean and std of the image to be able to normalize
    meanSlice= np.mean(Im)
    stdSlice=np.std(Im)
    ImCorrected=(Im-meanSlice)/stdSlice
    ImCorrected=ImCorrected-darkfield
    print('-----------------------  normalization correction done ----------------------- ')
    return ImCorrected



if __name__ == "__main__":
    print('test corrections start')



    Ir = spytIO.openImage('ref1-1.edf')
    Is = spytIO.openImage('samp1-1.edf')
    DF= spytIO.openImage('DF1-1.edf')


    correctedRef=registerRefAndSample(Ir,Is,1000)
    correctedRef=normalization(correctedRef,DF)
    refCorrectedOutputFileName = '/Users/helene/PycharmProjects/spytlab/output/correctedRef.edf'
    outputEdf = edf.EdfFile(refCorrectedOutputFileName, access='wb+')
    outputEdf.WriteImage({}, correctedRef)


    correctedSample=normalization(Is,DF)
    sampleCorrectedOutputFileName = '/Users/helene/PycharmProjects/spytlab/output/correctedSample.edf'
    outputEdf = edf.EdfFile(sampleCorrectedOutputFileName, access='wb+')
    outputEdf.WriteImage({}, correctedSample)

