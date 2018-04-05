# -*- coding: utf-8 -*-
"""
SpytLab speckle python lab
Author: helen labriet & Emmanuel brun
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


