from nd2reader import ND2reader
import simplejson as json

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as numpy

from ctypes import c_uint16

R = ND2reader("D:\\Jian\\Documents\\Projects\\myprojects\\ND2SDK\\nd2sdk-wrappers\\sampleND2\\sampleND2.nd2")

img = R.getImage(10)

#plt.imshow(img)
#plt.show()

#print(img)