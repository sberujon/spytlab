from skimage.feature import register_translation
from scipy.ndimage import fourier_shift
import numpy as np
import spytIO
import EdfFile as edf




def registerRefAndSample(ref,sample,precision):
    # correction of beam movementn
    shifts, error, phasediff = register_translation(sample, ref, precision)
    offset_image = fourier_shift(np.fft.fftn(ref), shifts)
    offset_image = np.fft.ifftn(offset_image)
    print ' the register correction shift is ( in pixels ) : '
    print shifts
    print ' ----------------------- registration correction done------------------------ '
    return offset_image.real

# def errorDetection (Ir, Is):
#     # correction of failed acquired  couple Ir and Is

#     if shifts> 10
#         Ir=IrError
#         Is=IsError
#         IrErrorOutputFileName = '/Users/helene/PycharmProjects/spytlab/output/IrError.edf'
#         outputEdf = edf.EdfFile(IrErrorOutputFileName, access='wb+')
#         outputEdf.WriteImage({}, correctedSample)
#     else
#         Ir=Ir
#         IrGoodOutputFileName = '/Users/helene/PycharmProjects/spytlab/output/IrGood.edf'
#         outputEdf = edf.EdfFile(IrGoodOutputFileName, access='wb+')
#         outputEdf.WriteImage({}, Ir)
#         Is=Is
#         IsGoodOutputFileName = '/Users/helene/PycharmProjects/spytlab/output/IsGood.edf'
#         outputEdf = edf.EdfFile(IsGoodOutputFileName, access='wb+')
#         outputEdf.WriteImage({}, Is)

    print ' ----------------------- error detection correction done------------------------ '


def normalization (Im, darkfield):
    # correction by flat or dark field
    #calculate mean and std of the image to be able to normalize
    meanIm= np.mean(Im)
    stdIm=np.std(Im)

    ImCorrected=(Im-meanIm)/stdIm

    ImCorrected=ImCorrected-darkfield
    Im=ImCorrected
    print '-----------------------  normalization correction done ----------------------- '
    return Im.real


if __name__ == "__main__":
    print 'test corrections start'



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

