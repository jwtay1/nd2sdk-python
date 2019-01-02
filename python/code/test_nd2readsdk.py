import os

dlldir = os.path.join(os.path.dirname(__file__), "..", "..", 'lib', 'win')
os.environ["PATH"] += os.pathsep + os.path.join(dlldir)

import nd2ReadSDK as nd2
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
import ctypes

testFP = Path("D:\\Jian\\Documents\\Projects\\myprojects\\ND2SDK\\nd2sdk-wrappers\\sampleND2\\sampleND2.nd2")

_fh = nd2.Lim_FileOpenForRead(str(testFP.resolve()))

attr = nd2.LIMATTRIBUTES()

res = nd2.Lim_FileGetAttributes(_fh, attr)
print(res)

md = nd2.LIMMETADATA_DESC()
res = nd2.Lim_FileGetMetadata(_fh, md)
print(res)

_buf_pic = nd2.LIMPICTURE()
res = nd2.Lim_InitPicture(_buf_pic, attr.uiWidth, attr.uiHeight, attr.uiBpcSignificant, attr.uiComp)
print(res)

localMD = nd2.LIMLOCALMETADATA()
res = nd2.Lim_FileGetImageData(_fh, 0, _buf_pic, localMD)
print(res)

_array_pic = ctypes.c_uint16 * attr.uiWidth * attr.uiHeight * attr.uiComp
_array_pic_p = _array_pic.from_address(_buf_pic.pImageData)

im = np.ndarray((attr.uiHeight, attr.uiWidth, attr.uiComp),
                np.uint16, _array_pic_p).copy()

plt.imshow(im[:,:,0])
plt.show()


nd2.Lim_DestroyPicture(_buf_pic)

res = nd2.Lim_FileClose(_fh)
print(res)
