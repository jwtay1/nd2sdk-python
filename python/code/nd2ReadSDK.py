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
    """ Structure to hold image data """
    _fields_ = [("uiWidth", LIMUINT),           # Image width in pixels
                ("uiHeight", LIMUINT),          # Image height in pixels
                ("uiBitsPerComp", LIMUINT),     # Number of bits per component 
                ("uiComponents", LIMUINT),      # Number of components per pixel
                ("uiWidthBytes", LIMSIZE),      # Number of bytes in memory/row
                ("uiSize", LIMSIZE),            # Size of image in memory
                ("pImageData", c_void_p)        # Pointer to image data
                ]

class LIMBINARYDESCRIPTOR(Structure):
    """ Describes a binary (masked) layer """
    _fields_ = [("wszName", LIMWCHAR * 256),          # Name of binary layer
                ("wszCompName", LIMWCHAR * 256),      # Name of bound component
                ("uiColorRGB", LIMUINT)         # Color of layer
                ]

class LIMBINARIES(Structure):
    """ Collection of binary layer descriptions """
    _fields_ = [("uiCount", LIMUINT),           #Number of layers
                 ("pDescriptors", LIMBINARYDESCRIPTOR * LIMMAXBINARIES)
                 ]
                 
class LIMPICTUREPLANE_DESC(Structure):
    """ Description of the channel (e.g. brightfield, mono) """
    _fields_ = [("uiCompCount", LIMUINT),   # Number of physical components
                ("uiColorRGB", LIMUINT),    # RGB color for display
                ("wszName", LIMWCHAR * 256),      # Name for display
                ("wszOCName", LIMWCHAR * 256),    # Name of Opt Configuration
                ("dEmissionWL", c_double)   # Emission wavelength
                ]

class LIMMETADATA_DESC (Structure):
    """ Acquisition metadata  """
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
    """ Description of file """
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
    _fields_ = [("uiExpType", LIMUINT),
                ("uiLoopSize", LIMUINT),    # Number of images in the loop
                ("dInterval", c_double)     # ms (for Time), um (for ZStack), 
                ]                           # -1.0 (for Multipoint
                
class LIMEXPERIMENT(Structure):
    _fields_ = [("uiLevelCount", LIMUINT),
                ("pAllocatedLevels", LIMEXPERIMENTLEVEL * LIMMAXEXPERIMENTLEVEL)
                ]

class LIMLOCALMETADATA(Structure):
    _fields_ = [("dTimeMSec", c_double),
                ("dXPos", c_double),
                ("dYPos", c_double),
                ("dZPos", c_double)
               ]

class LIMATTRIBUTES(Structure):
    """ Description of image """
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
    
    The returned object has the following attributes:

        +-------------------+---------------------------------------------+
        | Field             | Description                                 |
        +===================+=============================================+
        | uiWidth           | Width of images                             |
        +-------------------+---------------------------------------------+
        | uiWidthBytes      | Number of bytes per row                     |
        +-------------------+---------------------------------------------+
        | uiHeight          | Height of images                            |
        +-------------------+---------------------------------------------+
        | uiComp            | Number of components (channels)             |
        +-------------------+---------------------------------------------+
        | uiBpcInMemory     | Bits per component 8 or 16                  |
        +-------------------+---------------------------------------------+
        | uiBpcSignificant  | Bits per component used 8 .. 16             |
        +-------------------+---------------------------------------------+
        | uiSequenceCount   | Number of images in the sequences           |
        +-------------------+---------------------------------------------+
        | uiTileWidth       | If an image is tiled size of the tile/strip |
        +-------------------+ otherwise both zero                         |
        | uiTileHeight      |                                             |
        +-------------------+---------------------------------------------+
        | uiCompression     | 0 (lossless), 1 (lossy), 2 (None)           |
        +-------------------+---------------------------------------------+
        | uiQuality         | 0 (worst) - 100 (best)                      |
        +-------------------+---------------------------------------------+

    Args:
        fhandle (uint): Handle to open file
    
    Returns:
        limattr (LIMATTRIBUTES): Object containing file attributes

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
    
    The returned object has the following properties:
        double      dTimeStart;          // Absolute Time in JDN
        double      dAngle;              // Camera Angle
        double      dCalibration;        // um/px (0.0 = uncalibrated)
        double      dAspect;             // pixel aspect (always 1.0)
        LIMWCHAR    wszObjectiveName[256];
        double      dObjectiveMag;       // Optional additional information
        double      dObjectiveNA;        // dCalibration takes into accont all these
        double      dRefractIndex1;
        double      dRefractIndex2;
        double      dPinholeRadius;
        double      dZoom;
        double      dProjectiveMag;
        LIMUINT     uiImageType;         // 0 (normal), 1 (spectral)
        LIMUINT     uiPlaneCount;        // Number of logical planes (uiPlaneCount                                      <= uiComponentCount)
        LIMUINT     uiComponentCount;    // Number of physical components (same as                                      uiComp in LIMATTRIBUTES)
        LIMPICTUREPLANE_DESC pPlanes[LIMMAXPICTUREPLANES];

    Args:
        fhandle (uint): Handle to open file

    Returns:
        md (LIMMETADATA_DESC): Object containing file metadata

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
    Initializes a memory buffer for the API to return a picture. The values for the arguments can be retrieved using Lim_FileGetAttributes(). The resulting object must be destroyed using Lim_DestroyPicture() to free memory.

    bpicture has the following attributes:
        LIMUINT     uiWidth;           //width of the image in px. 
        LIMUINT     uiHeight;          //height of the image in px 
        LIMUINT     uiBitsPerComp;     //Number of bits per component (8, 10,                                    12, 14, 16). 
                                       //For binary images, use 32 bits. 
        LIMUINT     uiComponents;      //Number of components in every pixel 
                                         (any number up to 160 1:mono, 3:RGB)  
        LIMUINT     uiWidthBytes;      //Aligned to 4-byte (like windows BITMAP)
        LIMSIZE     uiSize;            //Size of the image in memory (= 
                                         uiWidthBytes * uiHeight).  
        void*       pImageData;        //Pointer to image data.  

    Args:
        width (uint): Image width in pixels
        height (uint): Image height in pixels
        bits_per_comp (uint): Bits per component
        num_comp (uint): Number of physical components

    Returns:
        bpicture (LIMPICTURE): Object with pointer to picture

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
        bpicture (LIMPICTURE): Object with pointer to picture
    
    Returns:
        None

    Raises:
        ND2SDKError: If error occurs destroying the picture object

    """
    
    limresult = _Lim_DestroyPicture(bpicture)

    if limresult != 0:
        raise ND2SDKError(limresult)

    return


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
        bpicture (LIMPICTURE): Picture object to hold data

    Returns:
        imgmd (LIMLOCALMEDATA): Object containing metadata of frame

    Raises:
        ND2SDKError: If error occurs reading the image

    """
    
    imgmd = LIMLOCALMETADATA()

    limresult = _Lim_FileGetImageData(fhandle, seq_index, bpicture, imgmd)

    if limresult != 0:
        raise ND2SDKError(limresult)

    return imgmd

# LIMFILEAPI LIMRESULT       Lim_FileGetImageRectData(LIMFILEHANDLE hFile, LIMUINT uiSeqIndex, LIMUINT uiDstTotalW, LIMUINT uiDstTotalH, LIMUINT uiDstX, LIMUINT uiDstY, LIMUINT uiDstW, LIMUINT uiDstH, void* pBuffer, LIMUINT uiDstLineSize, LIMINT iStretchMode, LIMLOCALMETADATA* pImgInfo);

# LIMFILEAPI LIMRESULT       Lim_FileGetBinaryDescriptors(LIMFILEHANDLE hFile, LIMBINARIES* pBinaries);
# LIMFILEAPI LIMRESULT       Lim_FileGetBinary(LIMFILEHANDLE hFile, LIMUINT uiSequenceIndex, LIMUINT uiBinaryIndex, LIMPICTURE* pPicture);

# LIMFILEAPI LIMUINT         Lim_GetSeqIndexFromCoords(LIMEXPERIMENT* pExperiment, LIMUINT* pExpCoords);
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

# LIMFILEAPI LIMRESULT       Lim_FileGetTextinfo(LIMFILEHANDLE hFile, LIMTEXTINFO* pFileTextinfo);

_Lim_FileGetExperiment = nd2sdk.Lim_FileGetExperiment
_Lim_FileGetExperiment.argtypes = [LIMFILEHANDLE, POINTER(LIMEXPERIMENT)]
_Lim_FileGetExperiment.restype = LIMRESULT

def Lim_FileGetExperiment(fhandle):
    """
    Returns metadata about the ND acquisition. 
    
    The returned object has the following attributes:

        uiLevelCount: Number of dimensions excl. Lambda (since Lim_FileGetImageData() always returns all channels)

        pAllocatedLevels: An array containing information about number of frames within each dimension. The array has the following attributes:

            uiExpType: Dimension type

            uiLoopSize: Number of images in loop
            dInterval: in milliseconds for time, um for z-stack and is undefined for multipoint

    Args:
        fhandle (uint): Handle to open file
    
    Returns:
        expmd (LIMEXPERIMENT): Object containing experiment metadata

    Raises:
        ND2SDKError: If error occurs

    """

    expmd = LIMEXPERIMENT()

    limresult = _Lim_FileGetExperiment(fhandle, expmd)
    
    if limresult != 0:
        raise ND2SDKError(limresult)

    return expmd    



# LIMFILEAPI LIMRESULT       Lim_FileGetExperiment(LIMFILEHANDLE hFile, LIMEXPERIMENT* pFileExperiment);

class ND2SDKError(Exception):

    def __init__(self, error_code):
        self.error_code = error_code
        
    def __str__(self):
        return repr("SDK returned error code {}:{}".format(self.error_code, LIM_ERR[self.error_code]))

