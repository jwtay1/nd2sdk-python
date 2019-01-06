""" Python wrapper for ND2 SDK v9.00

This module provides a wrapper for Python using 'ctypes' for the Nikon ND2 SDK v9.00. 

To get started, go to https://www.nd2sdk.com and download the appropriate SDK for your operating system. Extract the downloaded archive, then copy the required libraries to the 'lib' folder under this directory.

For Windows: Copy the files in the subdirectory SDK/bin/x64 (64-bit) or x86 (32-bit). The code only needs the DLL files (you can leave out the files starting with "Qt5")

For Mac: Copy the files in the subdirectory nd2sdk/nd2sdk.framework/Versions/1

"""

from ctypes import (c_int, c_uint32, c_uint64, c_float, c_char, c_char_p, 
    c_wchar, c_wchar_p, c_size_t, c_void_p, Structure, cdll, POINTER, c_uint, c_double)
import os

#Add the "lib" folder to the os path
libroot = os.path.join(os.path.dirname(__file__), "lib")
os.environ["PATH"] += os.pathsep + os.path.join(libroot)

#Use ctypes.cdll to load the libraries
platform = os.name

if platform == "nt":
    nd2sdk = cdll.LoadLibrary("v6_w32_nd2ReadSDK.dll")
elif platform == "posix":
    nd2sdk = cdll.LoadLibrary("nd2sdk")
elif platform == "linux":
    raise OSError('The ND2 SDK file downloads for Linux were disabled at writing.')
else:
    pass

#Typedefs
LIMWCHAR = c_wchar      # Wide-char (platform specific)
LIMWSTR = c_wchar_p     # Pointer to null-terminated wide-char array
LIMCWSTR = c_wchar_p    # Pointer to null-terminated const wide-char array

LIMUINT = c_uint32      # Unsigned integer 32-bit
LIMSIZE = c_size_t      # Memory Size type
LIMINT = c_uint32       # Integer 32-bit
LIMBOOL = c_int         # Integer boolean value {0, 1}
LIMRESULT = c_int       # Integer boolean values

LIMFILEHANDLE = c_int    # Opaque type representing an opened ND2 file

LIM_ERR = {
    0: "LIM_OK",
    -1: "LIM_ERR_UNEXPECTED",
    -2: "LIM_ERR_NOTIMPL",
    -3: "LIM_ERR_OUTOFMEMORY",
    -4: "LIM_ERR_INVALIDARG",
    -5: "LIM_ERR_NOINTERFACE",
    -6: "LIM_ERR_POINTER",
    -7: "LIM_ERR_HANDLE",
    -8: "LIM_ERR_ABORT",
    -9: "LIM_ERR_FAIL",
    -10: "LIM_ERR_ACCESSDENIED",
    -11: "LIM_ERR_OS_FAIL",
    -12: "LIM_ERR_NOTINITIALIZED",
    -13: "LIM_ERR_NOTFOUND",
    -14: "LIM_ERR_IMPL_FAILED",
    -15: "LIM_ERR_DLG_CANCELED",
    -16: "LIM_ERR_DB_PROC_FAILED",
    -17: "LIM_ERR_OUTOFRANGE",
    -18: "LIM_ERR_PRIVILEGES",
    -19: "LIM_ERR_VERSION"
}

LIMMAXBINARIES = 128
LIMMAXEXPERIMENTLEVEL = 8
LIMMAXPICTUREPLANES = 256
#define LIMMAXKEYLENGTH         32 
#define LIMMAXCUSTOMTAGS        32
# #define LIMLOOP_TIME             0
# #define LIMLOOP_MULTIPOINT       1
# #define LIMLOOP_Z                2
# #define LIMLOOP_OTHER            3
# #define LIMSTRETCH_QUICK    1
# #define LIMSTRETCH_SPLINES  2
# #define LIMSTRETCH_LINEAR   3


class LIMPICTURE(Structure):
    """ 
    Structure with image data 

    The image data is returned as a ctype pointer. To actually read the data, 
    create a ctype array that matches the size of the image (uiWidth * uiHeight * uiComponents).

    For an example, see :func:`Lim_FileGetImageData`
    
    Attributes:
        uiWidth (uint): Image width in pixels
        uiHeight (uint): Image height in pixels
        uiBitsPerComp (uint): Number of bits per component (channel)
        uiComponents (uint): Number of components per pixel
        uiWidthBytes (uint): Number of bytes per row
        uiSize (uint): Total number of bytes in memory
        pImageData (uint): Pointer to image data

    """

    _fields_ = [("uiWidth", LIMUINT),           # Image width in pixels
                ("uiHeight", LIMUINT),          # Image height in pixels
                ("uiBitsPerComp", LIMUINT),     # Number of bits per component 
                ("uiComponents", LIMUINT),      # Number of components per pixel
                ("uiWidthBytes", LIMSIZE),      # Number of bytes in memory/row
                ("uiSize", LIMSIZE),            # Size of image in memory
                ("pImageData", c_void_p)        # Pointer to image data
                ]

class LIMBINARYDESCRIPTOR(Structure):
    """ 
    Describes a binary (masked) layer

    Attributes:
        wszName (str): Name of binary layer
        wszCompName (str): Name of component the binary layer is bound to
        uiColorRGB (uint): Color of layer for display

    See also: :class:`LIMBINARIES`
    
    """

    _fields_ = [("wszName", LIMWCHAR * 256),          # Name of binary layer
                ("wszCompName", LIMWCHAR * 256),      # Name of bound component
                ("uiColorRGB", LIMUINT)         # Color of layer
                ]

class LIMBINARIES(Structure):
    """
    Structure with binary layer information

    Attributes:
        uiCount (uint): Number of binary layers
        pDescriptors (:class:`LIMBINARYDESCRIPTOR`): Binary layer description

    """

    _fields_ = [("uiCount", LIMUINT),           #Number of layers
                 ("pDescriptors", LIMBINARYDESCRIPTOR * LIMMAXBINARIES)
                 ]
                 
class LIMPICTUREPLANE_DESC(Structure):
    """ 
    Description of the channel (e.g. brightfield, mono) 

    Attributes:
        uiCompCount (uint): Number of channels
        uiColorRGB (uint): RGB color for display
        wszName (str): Name of channel for display
        wszOCName (str): Name of optical configuration
        dEmissionWL (double): Emission wavelength    
    
    """

    _fields_ = [("uiCompCount", LIMUINT),
                ("uiColorRGB", LIMUINT),
                ("wszName", LIMWCHAR * 256),
                ("wszOCName", LIMWCHAR * 256),
                ("dEmissionWL", c_double)
                ]

class LIMMETADATA_DESC (Structure):
    """ 
    Acquisition metadata  
    
    Attributes:
        dTimeStart (double):  Time in Julian Day Number (JDN)
        dAngle (double): Camera angle
        dCalibration (double): um/px (0.0 = uncalibrated)
        dAspect (double): pixel aspect (always 1.0)
        wszObjectiveName (str): Name of objective lens
        dObjectiveMag (double): Objective magnification
        dObjectiveNA (double): Objective NA
        dRefractIndex1 (double)
        dRefractIndex2 (double)
        dPinholeRadius (double): Pinhole radius
        dZoom (double)
        dProjectiveMag (double)
        uiImageType (uint): 0 (normal), 1 (spectral)
        uiPlaneCount (uint): Number of logical planes (uiPlaneCount <= uiComponentCount)
        uiComponentCount (uint): Number of physical components
        pPlanes (:class:`LIMPICTUREPLANE_DESC`)    
    
    """

    _fields_ = [("dTimeStart", c_double),       # Absolute Time in JDN
                ("dAngle", c_double),           # Camera Angle
                ("dCalibration", c_double),     # um/px (0.0 = uncalibrated)
                ("dAspect", c_double),          # pixel aspect (always 1.0)
                ("wszObjectiveName", LIMWCHAR * 256),
                ("dObjectiveMag", c_double), 
                ("dObjectiveNA", c_double),
                ("dRefractIndex1", c_double),
                ("dRefractIndex2", c_double),
                ("dPinholeRadius", c_double),
                ("dZoom", c_double),
                ("dProjectiveMag", c_double),
                ("uiImageType", LIMUINT),       # 0 (normal), 1 (spectral)
                ("uiPlaneCount", LIMUINT),      # Number of logical planes
                ("uiComponentCount", LIMUINT),  # Number of physical components
                ("pPlanes", LIMPICTUREPLANE_DESC * LIMMAXPICTUREPLANES)
                ]

class LIMTEXTINFO(Structure):
    """ 
    Additional text information

    Attributes:
        wszImageID (str)
        wszType (str)
        wszGroup (str)
        wszSampleID (str)
        wszAuthor (str)
        wszDescription (str)
        wszCapturing (str)
        wszSampling (str)
        wszDate (str)
        wszConclusion (str)
        wszInfo1 (str)
        wszInfo2 (str)
        wszOptics (str)
        wszAppVersion (str)
    
    """

    _fields_ = [("wszImageID", LIMWCHAR * 256) ,
                ("wszType", LIMWCHAR * 256),
                ("wszGroup", LIMWCHAR * 256),
                ("wszSampleID", LIMWCHAR * 256),
                ("wszAuthor", LIMWCHAR * 256),
                ("wszDescription", LIMWCHAR * 4096),
                ("wszCapturing", LIMWCHAR * 4096),
                ("wszSampling", LIMWCHAR * 256),
                ("wszDate", LIMWCHAR * 256),
                ("wszConclusion", LIMWCHAR * 256),
                ("wszInfo1", LIMWCHAR * 256),
                ("wszInfo2", LIMWCHAR * 256),
                ("wszOptics", LIMWCHAR * 256),
                ("wszAppVersion", LIMWCHAR * 256)
                ]

class LIMEXPERIMENTLEVEL(Structure):
    """
    Data structure to hold experiment level metadata

    The values for dInterval have the units milliseconds for time, um for z-stack and undefined (0.0) for multipoint.

    Attributes:
        uiExpType: Dimension type (0=time, 1=multipoint, 2=z, 3=other)
        uiLoopSize: Number of images in the dimension
        dInterval: Interval between each image in dimension

    """

    _fields_ = [("uiExpType", LIMUINT),
                ("uiLoopSize", LIMUINT),    # Number of images in the loop
                ("dInterval", c_double)     # ms (for Time), um (for ZStack), 
                ]                           # -1.0 (for Multipoint
                
class LIMEXPERIMENT(Structure):
    """
    Data structure to hold experimental metadata

    Wavelength is excluded because Lim_FileGetImageData() always returns all channels). For example, if uiLevelCount = 2, then the ND2 file has two additional dimensions apart from the wavelength.

    Attributes:
        uiLevelCount: Number of dimensions excl. wavelength
        pAllocatedLevels: Structure with information about dimensions
        
    See also: :class:`LIMEXPERIMENTLEVEL`
               
    """

    _fields_ = [("uiLevelCount", LIMUINT),
                ("pAllocatedLevels", LIMEXPERIMENTLEVEL * LIMMAXEXPERIMENTLEVEL)
                ]

class LIMLOCALMETADATA(Structure):
    """
    
    Attributes:
        dTimeMSec (double): Relative time [msec] from the first frame
        dXPos (double): Stage XPos
        dYPos (double): Stage YPos
        dZPos (double): Stage ZPos

    """

    _fields_ = [("dTimeMSec", c_double),
                ("dXPos", c_double),
                ("dYPos", c_double),
                ("dZPos", c_double)
               ]

class LIMATTRIBUTES(Structure):
    """ 
    Description of image 
    
    Attributes:
        uiWidth (uint): Width of images in pixels
        uiWidthBytes (uint): Line length
        uiHeight (uint): Height of images in pixels
        uiComp (uint): Number of components (channels)
        uiBpcInMemory (uint): Number of bits per component (8 or 16)
        uiBpcSignificant (uint): Number of significant bits per component
        uiSequenceCount (uint): Number of images in sequence
        uiTileWidth (uint): If an image is tiled size of the tile/strip
        uiTileHeight (uint)
        uiCompression (uint): 0 (lossless), 1 (lossy), 2 (None)
        uiQuality (uint): 0 (worst) - 100 (best)
    
    """

    _fields_ = [("uiWidth", LIMUINT),
                ("uiWidthBytes", LIMUINT),
                ("uiHeight", LIMUINT),
                ("uiComp", LIMUINT),
                ("uiBpcInMemory", LIMUINT),
                ("uiBpcSignificant", LIMUINT),
                ("uiSequenceCount", LIMUINT),
                ("uiTileWidth", LIMUINT),
                ("uiTileHeight", LIMUINT),
                ("uiCompression", LIMUINT),
                ("uiQuality", LIMUINT)]

class LIMFILEUSEREVENT(Structure):
    """

    Attributes:
        uiID (uint)
        dTime (double)
        wsType (str)
        wsDescription (str)

    """

    _fields_ = [("uiID", LIMUINT),
                ("dTime", c_double),
                ("wsType", LIMWCHAR * 128),
                ("wsDescription", LIMWCHAR * 256)
                ]


#Function calls

_Lim_FileOpenForRead = nd2sdk.Lim_FileOpenForRead
_Lim_FileOpenForRead.argtypes = [LIMCWSTR]
_Lim_FileOpenForRead.restype = LIMFILEHANDLE

def Lim_FileOpenForRead(filepath):
    """ 
    Opens an ND2 file for reading. 
    
    The opened file must be closed using Lim_FileClose().

    Args:
        filepath (str): String containing path to the ND2 file
    
    Returns:
        fhandle (uint): Handle to open file

    Raises:
        FileNotFoundError: If filepath does not point to an actual file
        ND2SDKError: If another error occurs

    """
    fhandle = _Lim_FileOpenForRead(filepath)

    if fhandle == 0:
        if not os.path.isfile(filepath):
            raise FileNotFoundError
        else:
            raise ND2SDKError(-9)

    return fhandle


_Lim_FileClose = nd2sdk.Lim_FileClose
_Lim_FileClose.argtypes = [LIMFILEHANDLE]
_Lim_FileClose.restype = LIMRESULT

def Lim_FileClose(fhandle):
    """
    Closes an open file to free up resources

    Args:
        fhandle (uint): Handle to open file

    Returns:
        result (int): 0 if function returned without error

    """
    result = _Lim_FileClose(fhandle)

    return result


_Lim_FileGetAttributes = nd2sdk.Lim_FileGetAttributes
_Lim_FileGetAttributes.argtypes = [LIMFILEHANDLE, POINTER(LIMATTRIBUTES)]
_Lim_FileGetAttributes.restype = LIMRESULT

def Lim_FileGetAttributes(fhandle):
    """
    Returns basic file attributes which are common to all frames

    Args:
        fhandle (uint): Handle to open file
    
    Returns:
        limattr (:class:`LIMATTRIBUTES`): Object containing file attributes

    """
    limattr = LIMATTRIBUTES()

    limresult = _Lim_FileGetAttributes(fhandle, limattr)

    if limresult != 0:
        raise ND2SDKError(limresult)
       
    return limattr


_Lim_FileGetMetadata = nd2sdk.Lim_FileGetMetadata
_Lim_FileGetMetadata.argtypes = [LIMFILEHANDLE, POINTER(LIMMETADATA_DESC)]
_Lim_FileGetMetadata.restype = LIMRESULT

def Lim_FileGetMetadata(fhandle):
    """
    Get file metadata

    Args:
        fhandle (uint): Handle to open file

    Returns:
        md (:class:`LIMMETADATA_DESC`): Object containing file metadata

    """
    md = LIMMETADATA_DESC()

    limresult = _Lim_FileGetMetadata(fhandle, md)

    if limresult != 0:
        raise ND2SDKError(limresult)

    return md

_Lim_InitPicture = nd2sdk.Lim_InitPicture
_Lim_InitPicture.argtypes = [POINTER(LIMPICTURE), LIMUINT, LIMUINT, LIMUINT, LIMUINT]
_Lim_InitPicture.restype = LIMSIZE

def Lim_InitPicture(width, height, bits_per_comp, num_comp):
    """
    Initializes a memory buffer for the API to return a picture. The values for the arguments can be retrieved using :func:`Lim_FileGetAttributes`. The resulting object must be destroyed using :func:`Lim_FileGetAttributes` to free memory.

    Args:
        width (uint): Image width in pixels
        height (uint): Image height in pixels
        bits_per_comp (uint): Bits per component
        num_comp (uint): Number of physical components

    Returns:
        bpicture (:class:`LIMPICTURE`): Object with pointer to picture

    Raises:
        ND2SDKError: If error occurs initializing the picture object

    """
    bpicture = LIMPICTURE()
    limresult = _Lim_InitPicture(bpicture, width, height, bits_per_comp, 
                                        num_comp)

    # if limresult != 0:
    #     raise ND2SDKError(limresult)                                     

    return bpicture


_Lim_DestroyPicture = nd2sdk.Lim_DestroyPicture
_Lim_DestroyPicture.argtypes = [POINTER(LIMPICTURE)]
_Lim_DestroyPicture.restype = None

def Lim_DestroyPicture(bpicture):
    """
    Frees memory used to store picture data

    Args:
        bpicture (:class:`LIMPICTURE`): Object with pointer to picture
    
    Returns:
        None

    Raises:
        ND2SDKError: If error occurs destroying the picture object

    """
    
    _Lim_DestroyPicture(bpicture)

    return None


_Lim_FileGetImageData = nd2sdk.Lim_FileGetImageData
_Lim_FileGetImageData.argtypes = [LIMFILEHANDLE, LIMUINT, POINTER(LIMPICTURE), POINTER(LIMLOCALMETADATA)]
_Lim_FileGetImageData.restype = LIMRESULT

def Lim_FileGetImageData(fhandle, seq_index, bpicture):
    """
    Populates picture object with data
    
    Note: The picture object must be created using Lim_InitPicture().

    Args:
        fhandle (uint): Handle to open file
        seq_index (uint): Sequence index of frame
        bpicture (:class:`LIMPICTURE`): Picture object to hold data

    Returns:
        imgmd (:class:`LIMLOCALMEDATA`): Object containing metadata of frame

    Raises:
        ND2SDKError: If error occurs reading the image

    """
    
    imgmd = LIMLOCALMETADATA()

    limresult = _Lim_FileGetImageData(fhandle, seq_index, bpicture, imgmd)

    if limresult != 0:
        raise ND2SDKError(limresult)

    return imgmd


_Lim_FileGetExperiment = nd2sdk.Lim_FileGetExperiment
_Lim_FileGetExperiment.argtypes = [LIMFILEHANDLE, POINTER(LIMEXPERIMENT)]
_Lim_FileGetExperiment.restype = LIMRESULT

def Lim_FileGetExperiment(fhandle):
    """
    Returns metadata about the ND acquisition. 

    Args:
        fhandle (uint): Handle to open file
    
    Returns:
        expmd (:class:`LIMEXPERIMENT`): Object containing experiment metadata

    Raises:
        ND2SDKError: If error occurs reading the metadata

    """

    expmd = LIMEXPERIMENT()

    limresult = _Lim_FileGetExperiment(fhandle, expmd)
    
    if limresult != 0:
        raise ND2SDKError(limresult)

    return expmd    

_Lim_GetSeqIndexFromCoords = nd2sdk.Lim_GetSeqIndexFromCoords
_Lim_GetSeqIndexFromCoords.argtypes = [POINTER(LIMEXPERIMENT), POINTER(LIMUINT)]
_Lim_GetSeqIndexFromCoords.restype = LIMUINT

def Lim_GetSeqIndexFromCoords(handle_or_md, *coords):
    """
    Returns the index of an image specified by its coordinates

    The first argument can either be the handle to an open file or the
    structure returned by using :func:`Lim_FileGetExperiment`. This allows the  function to avoid requiring an additional call to :func:`Lim_FileGetExperiment` if the metadata already exists.
        
    The expected coordinates should be in the following sequence: Time, Multipoint (either XY-location or series), Zstep, Other. The coordinates are zero-based, i.e. the first timepoint is at coordinate 0.

    Args:
        hdl_or_md (uint or structure): Handle to open file or metadata
        *coords: Coordinates of the image
    
    Returns:
        seq_index (uint): Index of the image

    Raises:
        ValueError: If the requested coordinate does not exist

    """

    if type(handle_or_md) == int:
        expmd = Lim_FileGetExperiment(handle_or_md)
    else:
        expmd = handle_or_md

    #Check that the coordinates supplied are valid
    maxValues = [0, 0, 0, 0]
    for iL in range(expmd.uiLevelCount):
        maxValues[expmd.pAllocatedLevels[iL].uiExpType] = expmd.pAllocatedLevels[iL].uiLoopSize - 1

    for ii in range(len(coords)):
        if coords[ii] > maxValues[ii]:
            raise ValueError("Coordinate {} exceeds image dimensions (requested {}, max {})".format(ii, coords[ii], maxValues[ii]))

    #Convert the coords into a c_uint array
    coords_arr = (c_uint * 4)(*coords)
    
    seq_index = _Lim_GetSeqIndexFromCoords(expmd, coords_arr)

    return seq_index

_Lim_FileGetBinaryDescriptors = nd2sdk.Lim_FileGetBinaryDescriptors
_Lim_FileGetBinaryDescriptors.argtypes = [LIMFILEHANDLE, POINTER(LIMBINARIES)]
_Lim_FileGetBinaryDescriptors.restype = LIMRESULT

def Lim_FileGetBinaryDescriptors(fhandle):
    """
    Returns metadata about the binary layers

    Args:
        fhandle (uint): Handle to open file

    Returns:
        binaries (:class:`LIMBINARIES`): Structure with information about the binary layers
    
    Raises:
        ND2SDKError: If any error occurs retrieving the descriptors

    """

    binaries = LIMBINARIES()

    limresult = _Lim_FileGetBinaryDescriptors(fhandle, binaries)

    if limresult != 0:
        raise ND2SDKError(limresult)

    return binaries

_Lim_FileGetBinary = nd2sdk.Lim_FileGetBinary
_Lim_FileGetBinary.argtypes = [LIMFILEHANDLE, LIMUINT, LIMUINT, POINTER(LIMPICTURE)]
_Lim_FileGetBinary.restype = LIMRESULT

def Lim_FileGetBinary(fhandle, seq_index, bin_index, bpicture):
    """
    Retrieves an image from a binary layer

    Args:
        fhandle (uint): Handle to open file
        seq_index (uint): Sequence index of frame
        bin_index(uint): Index of binary layer
        bpicture (:class:`LIMPICTURE`): Picture object created using :func:Lim_InitPicture
        
    Returns:
        None

    Raises:
        ND2SDKError: If error occurs while reading the binary layers

    """

    limresult = nd2sdk._Lim_FileGetBinary(fhandle,
                                          seq_index,
                                          bin_index,
                                          bpicture)

    if limresult != 0:
        raise ND2SDKError(limresult)
    
    return None


_Lim_FileGetTextinfo = nd2sdk.Lim_FileGetTextinfo
_Lim_FileGetTextinfo.argtypes = [LIMFILEHANDLE, POINTER(LIMTEXTINFO)]
_Lim_FileGetTextinfo.restype = LIMRESULT

def Lim_FileGetTextinfo(fhandle):
    """
    Returns additional text info from the ND2 file

    The text info is optional and may not be populated in the file.

    Args:
        fhandle (uint): Handle to open file

    Returns:
        file_text_info (:class:`LIMTEXTINFO`): Text info from file

    Raises:
        ND2SDKError: If any error occurs

    """

    file_text_info = LIMTEXTINFO()

    limresult = _Lim_FileGetTextinfo(fhandle, file_text_info)

    if limresult != 0:
        raise ND2SDKError(limresult)

    return file_text_info


class ND2SDKError(Exception):
    """ Generic exception for errors thrown by SDK """

    def __init__(self, error_code):
        """

        Args:
            error_code (int): Error code returned by the SDK call
        
        Attributes:
            __str__: Message with the LIM_ERR value of the error_code

        """
        self.error_code = error_code
        
    def __str__(self):
        return repr("SDK returned error code {}:{}".format(self.error_code, LIM_ERR[self.error_code]))





#Additional functions (not yet converted)

# LIMFILEAPI LIMRESULT       Lim_FileGetImageRectData(LIMFILEHANDLE hFile, LIMUINT uiSeqIndex, LIMUINT uiDstTotalW, LIMUINT uiDstTotalH, LIMUINT uiDstX, LIMUINT uiDstY, LIMUINT uiDstW, LIMUINT uiDstH, void* pBuffer, LIMUINT uiDstLineSize, LIMINT iStretchMode, LIMLOCALMETADATA* pImgInfo);

# LIMFILEAPI void            Lim_GetCoordsFromSeqIndex(LIMEXPERIMENT* pExperiment, LIMUINT uiSeqIdx, LIMUINT* pExpCoords);
# LIMFILEAPI LIMRESULT       Lim_GetMultipointName(LIMFILEHANDLE hFile, LIMUINT uiPointIdx, LIMWSTR wstrPointName);
# LIMFILEAPI LIMINT          Lim_GetZStackHome(LIMFILEHANDLE hFile);
# LIMFILEAPI LIMRESULT       Lim_GetLargeImageDimensions(LIMFILEHANDLE hFile, LIMUINT* puiXFields, LIMUINT* puiYFields, double* pdOverlap);

# LIMFILEAPI LIMRESULT       Lim_GetRecordedDataInt(LIMFILEHANDLE hFile, LIMCWSTR wszName, LIMINT uiSeqIndex, LIMINT *piData);
# LIMFILEAPI LIMRESULT       Lim_GetRecordedDataDouble(LIMFILEHANDLE hFile, LIMCWSTR wszName, LIMINT uiSeqIndex, double* pdData);
# LIMFILEAPI LIMRESULT       Lim_GetRecordedDataString(LIMFILEHANDLE hFile, LIMCWSTR wszName, LIMINT uiSeqIndex, LIMWSTR wszData);
# LIMFILEAPI LIMRESULT       Lim_GetNextUserEvent(LIMFILEHANDLE hFile, LIMUINT *puiNextID, LIMFILEUSEREVENT* pEventInfo);

# LIMFILEAPI LIMINT          Lim_GetCustomDataCount(LIMFILEHANDLE hFile);
# LIMFILEAPI LIMRESULT       Lim_GetCustomDataInfo(LIMFILEHANDLE hFile, LIMINT uiCustomDataIndex, LIMWSTR wszName, LIMWSTR wszDescription, LIMINT *piType, LIMINT *piFlags);
# LIMFILEAPI LIMRESULT       Lim_GetCustomDataDouble(LIMFILEHANDLE hFile, LIMINT uiCustomDataIndex, double* pdData);
# LIMFILEAPI LIMRESULT       Lim_GetCustomDataString(LIMFILEHANDLE hFile, LIMINT uiCustomDataIndex, LIMWSTR wszData, LIMINT *piLength);

# LIMFILEAPI LIMRESULT       Lim_GetStageCoordinates(LIMFILEHANDLE hFile, LIMUINT uiPosCount, LIMUINT* puiSeqIdx, LIMUINT* puiXPos, LIMUINT* puiYPos, double* pdXPos, double *pdYPos, double *pdZPos, LIMINT iUseAlignment);
# LIMFILEAPI LIMRESULT       Lim_SetStageAlignment(LIMFILEHANDLE hFile, LIMUINT uiPosCount, double* pdXSrc, double* pdYSrc, double* pdXDst, double *pdYDst);
# LIMFILEAPI LIMRESULT       Lim_GetAlignmentPoints(LIMFILEHANDLE hFile, LIMUINT* puiPosCount, LIMUINT* puiSeqIdx, LIMUINT* puiXPos, LIMUINT* puiYPos, double *pdXPos, double *pdYPos);

