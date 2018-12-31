#Test code for the ND2 SDK Python wrapper


#Test memory leak - tracemalloc (https://docs.python.org/3/library/tracemalloc.html)

from pathlib import Path
import nd2sdk_wrapper as h
from ctypes import *

tmpFilePath = Path("C:/Users/Jian Tay/Downloads/fluorescentBeads.nd2").resolve()
tmpFilePath = str(tmpFilePath)

handle = h.Lim_FileOpenForRead(tmpFilePath)

attributes = h.Lim_FileGetAttributes(handle)

print(attributes)

h.Lim_FileFreeString(attributes)

nFrames = h.Lim_FileGetSeqCount(handle)
print(nFrames)

result = h.Lim_FileClose(handle)