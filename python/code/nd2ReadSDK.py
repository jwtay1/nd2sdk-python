from ctypes import (c_int, c_uint32, c_uint64, c_float, c_char, c_char_p, 
    c_wchar, c_wchar_p, c_size_t, c_void_p, Structure, cdll, POINTER, c_uint, c_double)
from pathlib import Path


libPath = Path(__file__).parent / ".." / ".." / "lib" / "win" / "v6_w32_nd2ReadSDK.dll"
print(libPath.resolve(strict = True))

nd2api = cdll.LoadLibrary(str(libPath.resolve()))

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


class LIMPICTURE (Structure):
    _fields_ = [("uiWidth", LIMUINT),
                ("uiHeight", LIMUINT),
                ("uiBitsPerComp", LIMUINT),
                ("uiComponents", LIMUINT),
                ("uiWidthBytes", LIMSIZE),
                ("uiSize", LIMSIZE),
                ("pImageData", c_void_p)                
                ]

# typedef struct _LIMBINARYDESCRIPTOR
# {
#    LIMWCHAR wszName[256];
#    LIMWCHAR wszCompName[256];       // name of component, or empty string if this binary layer is unbound
#    LIMUINT uiColorRGB;
# } LIMBINARYDESCRIPTOR;

# typedef struct _LIMBINARIES
# {
#    LIMUINT     uiCount;
#    LIMBINARYDESCRIPTOR pDescriptors[LIMMAXBINARIES];
# } LIMBINARIES;

# #define LIMMAXPICTUREPLANES    256

# typedef struct _LIMPICTUREPLANE_DESC
# {
#    LIMUINT     uiCompCount;         // Number of physical components
#    LIMUINT     uiColorRGB;          // RGB color for display
#    LIMWCHAR    wszName[256];        // Name for display
#    LIMWCHAR    wszOCName[256];      // Name of the Optical Configuration
#    double      dEmissionWL;
# } LIMPICTUREPLANE_DESC;

# typedef struct _LIMMETADATA_DESC
# {
#    double      dTimeStart;          // Absolute Time in JDN
#    double      dAngle;              // Camera Angle
#    double      dCalibration;        // um/px (0.0 = uncalibrated)
#    double      dAspect;             // pixel aspect (always 1.0)
#    LIMWCHAR    wszObjectiveName[256];
#    double      dObjectiveMag;       // Optional additional information
#    double      dObjectiveNA;        // dCalibration takes into accont all these
#    double      dRefractIndex1;
#    double      dRefractIndex2;
#    double      dPinholeRadius;
#    double      dZoom;
#    double      dProjectiveMag;
#    LIMUINT     uiImageType;         // 0 (normal), 1 (spectral)
#    LIMUINT     uiPlaneCount;        // Number of logical planes (uiPlaneCount <= uiComponentCount)
#    LIMUINT     uiComponentCount;    // Number of physical components (same as uiComp in LIMFILEATTRIBUTES)
#    LIMPICTUREPLANE_DESC pPlanes[LIMMAXPICTUREPLANES];
# } LIMMETADATA_DESC;

class LIMPICTUREPLANE_DESC (Structure):
    _fields_ = [("uiCompCount", LIMUINT),
                ("uiColorRGB", LIMUINT),
                ("wszName", LIMWCHAR),
                ("wszOCName", LIMWCHAR),
                ("dEmissionWL", c_double)]

class LIMMETADATA_DESC (Structure):
    _fields_ = [("dTimeStart", c_double),
                ("dAngle", c_double),
                ("dCalibration", c_double),
                ("dAspect", c_double),
                ("wszObjectiveName", LIMWCHAR),
                ("dObjectiveMag", c_double),
                ("dObjectiveNA", c_double),
                ("dRefractIndex1", c_double),
                ("dRefractIndex2", c_double),
                ("dPinholeRadius", c_double),
                ("dZoom", c_double),
                ("dProjectiveMag", c_double),
                ("uiImageType", LIMUINT),
                ("uiPlaneCount", LIMUINT),
                ("uiComponentCount", LIMUINT),
                ("pPlanes", LIMPICTUREPLANE_DESC * 255)
    ]

# typedef struct _LIMTEXTINFO
# {
#    LIMWCHAR wszImageID[256];
#    LIMWCHAR wszType[256];
#    LIMWCHAR wszGroup[256];
#    LIMWCHAR wszSampleID[256];
#    LIMWCHAR wszAuthor[256];
#    LIMWCHAR wszDescription[4096];
#    LIMWCHAR wszCapturing[4096];
#    LIMWCHAR wszSampling[256];
#    LIMWCHAR wszLocation[256];
#    LIMWCHAR wszDate[256];
#    LIMWCHAR wszConclusion[256];
#    LIMWCHAR wszInfo1[256];
#    LIMWCHAR wszInfo2[256];
#    LIMWCHAR wszOptics[256];
#    LIMWCHAR wszAppVersion[256];
# } LIMTEXTINFO;


# #define LIMLOOP_TIME             0
# #define LIMLOOP_MULTIPOINT       1
# #define LIMLOOP_Z                2
# #define LIMLOOP_OTHER            3

# #define LIMMAXEXPERIMENTLEVEL    8

# typedef struct _LIMEXPERIMENTLEVEL
# {
#    LIMUINT uiExpType;            // see LIMLOOP_TIME etc.
#    LIMUINT  uiLoopSize;          // Number of images in the loop
#    double   dInterval;           // ms (for Time), um (for ZStack), -1.0 (for Multipoint)
# } LIMEXPERIMENTLEVEL;

# typedef struct _LIMEXPERIMENT
# {
#    LIMUINT  uiLevelCount;
#    LIMEXPERIMENTLEVEL pAllocatedLevels[LIMMAXEXPERIMENTLEVEL];
# } LIMEXPERIMENT;

class LIMLOCALMETADATA(Structure):
    _fields_ = [("dTimeMSec", c_double),
                ("dXPos", c_double),
                ("dYPos", c_double),
                ("dZPos", c_double)
               ]

class LIMATTRIBUTES (Structure):
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


# typedef struct _LIMFILEUSEREVENT
# {
#    LIMUINT    uiID;
#    double     dTime;       
#    LIMWCHAR   wsType[128]; 
#    LIMWCHAR   wsDescription[256];
   
# } LIMFILEUSEREVENT;

# #define LIMSTRETCH_QUICK    1
# #define LIMSTRETCH_SPLINES  2
# #define LIMSTRETCH_LINEAR   3


Lim_FileOpenForRead = nd2api.Lim_FileOpenForRead
Lim_FileOpenForRead.argtypes = [LIMCWSTR]
Lim_FileOpenForRead.restype = LIMFILEHANDLE

Lim_FileClose = nd2api.Lim_FileClose
Lim_FileClose.argtypes = [LIMFILEHANDLE]
Lim_FileClose.restype = LIMRESULT

Lim_FileGetAttributes = nd2api.Lim_FileGetAttributes
Lim_FileGetAttributes.argtypes = [LIMFILEHANDLE, POINTER(LIMATTRIBUTES)]
Lim_FileGetAttributes.restype = LIMRESULT

Lim_FileGetMetadata = nd2api.Lim_FileGetMetadata
Lim_FileGetMetadata.argtypes = [LIMFILEHANDLE, POINTER(LIMMETADATA_DESC)]
Lim_FileGetMetadata.restype = LIMRESULT

Lim_InitPicture = nd2api.Lim_InitPicture
Lim_InitPicture.argtypes = [POINTER(LIMPICTURE), LIMUINT, LIMUINT, LIMUINT, LIMUINT]
Lim_InitPicture.restype = LIMSIZE

Lim_DestroyPicture = nd2api.Lim_DestroyPicture
Lim_DestroyPicture.argtypes = [POINTER(LIMPICTURE)]
Lim_DestroyPicture.restype = None

Lim_FileGetImageData = nd2api.Lim_FileGetImageData
Lim_FileGetImageData.argtypes = [LIMFILEHANDLE, LIMUINT, POINTER(LIMPICTURE), POINTER(LIMLOCALMETADATA)]
Lim_FileGetImageData.restype = LIMRESULT




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

# #endif // __ND2READSDK_H__


# LIMFILEAPI LIMRESULT       Lim_FileGetTextinfo(LIMFILEHANDLE hFile, LIMTEXTINFO* pFileTextinfo);
# LIMFILEAPI LIMRESULT       Lim_FileGetExperiment(LIMFILEHANDLE hFile, LIMEXPERIMENT* pFileExperiment);