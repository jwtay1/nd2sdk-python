import nd2sdk_wrapper as nd2
import simplejson as json
from pathlib import Path
from ctypes import c_uint16
import numpy as np

class ND2reader:
    """  Class to read ND2 files

    ND2reader is a class to read ND2 files created by a 
    Nikon microscope. The class uses the official ND2 SDK 
    libraries.

    Atrributes:


    Parameters:
        path_to_file (str): Path to the ND2 file
    """

    __fh = None   #File handle
    __buf_picture = None
    __buf_picture_array = None

    heightPx = 0
    widthPx = 0
    sizeC = 0
    channels = []

    bpc = 0
    numComponents = 0
    widthBytes = 0

    metadata = 0

    def __init__(self, pathIn):
        """ Test for documentation

            Constructor for the nd2reader class

        """

        fpath = Path(pathIn).resolve()
        fpath = str(fpath)
        
        #Open the file for reading
        self.__fh = nd2.Lim_FileOpenForRead(fpath)

        #Get file attributes
        byteAttrib = nd2.Lim_FileGetAttributes(self.__fh)
        attributes = json.loads(byteAttrib.decode())
        print(json.dumps(attributes, sort_keys=True, indent=4 * ' '))
        
        #res = nd2.Lim_FileFreeString(byteAttrib)
        #print("e")

        self.bpc = attributes["bitsPerComponentSignificant"]
        self.numComponents = attributes["componentCount"]
        self.widthBytes = attributes["widthBytes"]

        #Get file metadata
        byteMetadata = nd2.Lim_FileGetMetadata(self.__fh)
        self.metadata = json.loads(byteMetadata.decode())
        #print(json.dumps(self.metadata, sort_keys=True, indent=4 * ' '))

        #res = nd2.Lim_FileFreeString(byteMetadata)

        self.sizeC = self.metadata["contents"]["channelCount"]

        for channel in self.metadata["channels"]:
            self.channels.append(channel["channel"]["name"])

        #Update class attributes
        self.widthPx = attributes["widthPx"]
        self.heightPx = attributes["heightPx"]

        #Initialize a buffer to read the picture
        self.__buf_picture = nd2.LIMPICTURE()
        szPicture = nd2.Lim_InitPicture(self.__buf_picture,
                                        self.widthPx,
                                        self.heightPx,
                                        self.bpc,
                                        self.numComponents)

        print(szPicture)


    def __del__(self):
        """ Deconstructor

        """

        res = nd2.Lim_FileClose(self.__fh)

        if self.__buf_picture is not None:
            nd2.Lim_DestroyPicture(self.__buf_picture)
        print('Destroyed.')



    def getImage(self, seqIndex):
        """ Returns the requested image

        Just a test for Sphinx
        """
        res = nd2.Lim_FileGetImageData(self.__fh, seqIndex, self.__buf_picture)

        print(res)

        #Generate an output array
        arr = c_uint16 * (self.heightPx * self.widthPx * self.numComponents)

        im = np.ndarray((self.heightPx, self.widthPx), np.uint16,
                        arr.from_address(self.__buf_picture.pImageData)).copy()

        return im

        