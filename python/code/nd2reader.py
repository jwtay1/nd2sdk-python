import nd2sdk_wrapper as nd2
import simplejson as json
from pathlib import Path
from ctypes import c_uint16, pointer, c_uint, POINTER, cast
import numpy as np

class ND2reader:
    """  Class to read ND2 files

    ND2reader is a class to read ND2 files created by a 
    Nikon microscope. The class uses the official ND2 SDK 
    libraries and requires the "nd2sdk_wrapper" module. 

    """

    def __init__(self, pathIn):
        """ 
        Attributes
        ----------
        bitsPerComponent : int
            Number of bits per component (channel) of an image
        heightPx : int
            Height of image in pixels
        widthPx : int
            Width of image in pixels
        metadata : dict
            Full metadata of file (File attributes and metadata)
        frameCount : int
            Number of frames

        Parameters
        ----------
        pathIn : str
            Path to a valid ND2 file            

        """

        #Define instance variables
        self._fh = None   #File handle
        self._struct_picture = nd2.LIMPICTURE()  #Picture struct
        self.metadata = {}

        #Open the file for reading
        fpath = Path(pathIn).resolve(strict = True)
        fpath = str(fpath)
        self._fh = nd2.Lim_FileOpenForRead(fpath)

        #Get metadata
        fileAttr = nd2.Lim_FileGetAttributes(self._fh)
        self.metadata = json.loads(fileAttr.decode())
        fileMetadata = nd2.Lim_FileGetMetadata(self._fh)
        self.metadata.update(json.loads(fileMetadata.decode()))

        #Populate attributes
        self.frameCount = nd2.Lim_FileGetSeqCount(self._fh)
        self.coordSize = nd2.Lim_FileGetCoordSize(self._fh)
        self.experiment = nd2.Lim_FileGetExperiment(self._fh)

        #Initialize the picture buffer
        self._p_size = nd2.Lim_InitPicture(self._struct_picture,
                                             self.widthPx,
                                            self.heightPx,
                                            16,
                                            1)

        #arr_size = self.heightPx * self.widthPx * self.componentCount
        #arr = c_uint16 * arr_size
        #self._buf_picture = arr.from_address(self._struct_picture.pImageData)

    def printFrameMetadata(self, seqIndex):

        fm = nd2.Lim_FileGetFrameMetadata(self._fh, seqIndex)
        jsObj = json.loads(fm.decode())
        print(json.dumps(jsObj, sort_keys = True))

    def __del__(self):
        """
        
        Closes the ND2 file (if open)

        """

        nd2.Lim_FileClose(self._fh)
        nd2.Lim_DestroyPicture(self._struct_picture)

    def getImage(self, seqIndex):
        """ Returns the requested image

        """

        result = nd2.Lim_FileGetImageData(self._fh, seqIndex,                                         self._struct_picture)

        print(result)
        print(nd2.LIM_ERR[result])



    @property
    def bitsPerComponent(self):
        return self.metadata["bitsPerComponentSignificant"]

    @property
    def heightPx(self):
        return self.metadata["heightPx"]

    @property
    def widthPx(self):
        return self.metadata["widthPx"]

    @property
    def channelCount(self):
        return self.metadata["contents"]["channelCount"]
    
    @property
    def componentCount(self):
        return self.metadata["componentCount"]

    @property
    def channels(self):
        """ Return channel name and index as dict """

        ch = {}
        for chInfo in self.metadata["channels"]:
             ch[chInfo["channel"]["name"]] = chInfo["channel"]["index"]

        return ch
