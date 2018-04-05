# -*- coding: utf-8 -*-
"""
SpytLab speckle python lab
Author: Helene Labriet & Emmanuel Brun
Date: April 2018
"""

import EdfFile as edf
from PIL import Image
import numpy as np


def openImage(filename):
    if filename.endswith('.edf'):
        im = edf.EdfFile(filename, access='rb')
        imarray = im.GetData(0)
    else :
        imarray = Image.open(filename)
        imarray = np.array(imarray)

    return imarray

def openSeq(filename):


