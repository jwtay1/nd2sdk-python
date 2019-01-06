import nd2ReadSDK as nd2

from pathlib import Path
from ctypes import c_uint16, pointer, c_uint, POINTER, cast
import numpy as np

class ND2reader:
    """  
    Class to read ND2 files

    ND2reader is a class to read ND2 files created by a 
    Nikon microscope. The class uses the official ND2 SDK 
    libraries v9.0.

    """

    def __init__(self, pathIn):
        """ 
        Attributes:        
            bitsPerComponent (int): Number of bits per component (channel) of                           an image
            heightPx (int): Height of image in pixels
            widthPx (int): Width of image in pixels
            frameCount (int): Number of frames

        Returns:
            pathIn (str): Path to a valid ND2 file            

        """
       
        if isinstance(pathIn, str):
            self.filepath = Path(pathIn).resolve(strict = True)
        elif isinstance(pathIn, Path):
            self.filepath = pathIn
        else:
            raise TypeError("Expected input to be a string or a Path object")

        self._fhandle = nd2.Lim_FileOpenForRead(str(self.filepath))

        #Get file metadata
        limattributes = nd2.Lim_FileGetAttributes(self._fhandle)

        self.widthPx = limattributes.uiWidth
        self.heightPx = limattributes.uiHeight
        self.bitsPerComponent = limattributes.uiBpcInMemory
        self.numChannels = limattributes.uiComp

        print(type(limattributes.uiWidthBytes))

        #Initialize a read buffer for the picture
        self._bpicture = nd2.Lim_InitPicture(self.widthPx, self.heightPx, 
                                             self.bitsPerComponent, 
                                             self.numChannels)

        #Initialize a pointer to the picture buffer
        self._bpicture_ptr = (c_uint16 * self.widthPx * self.heightPx * self.numChannels).from_address(self._bpicture.pImageData)


    def __del__(self):
        """
        
        Closes the ND2 file (if open)

        """
        nd2.Lim_DestroyPicture(self._bpicture)
        nd2.Lim_FileClose(self._fhandle)
        
    def getImage(self, *index):
        """
        Returns the specified image as a numpy ndarray

        Note that the API always returns all channels of the specified image at once.

        Args:
            *index (uint): Either image coordinates or index

        Returns:
            np_array: A numpy ND array containing the image

        """

        if len(index) == 1:
            seq_index = index[0]
        else:
            seq_index = nd2.Lim_GetSeqIndexFromCoords(self._fhandle, *index)

        #Retrieve the image
        imgMD = nd2.Lim_FileGetImageData(self._fhandle, seq_index, self._bpicture)

        #Set the number of significant bits
        if self.bitsPerComponent == 16:
            np_bits = np.uint16
        elif self.bitsPerComponent == 8:
            np_bits = np.uint8
        else:
            np_bits = np.uint16 #By default set to uint16

        np_array = np.ndarray((self.heightPx, self.widthPx, self.numChannels),
                              np_bits, self._bpicture_ptr).copy()

        return np_array