""" Python wrapper for the ND2 SDK

This module uses the ctypes package to generate a Python interface for the ND2 SDK libraries.

The libraries are included in this repository but are also available in their original forms from https://www.nd2sdk.com/. The current supported version is 0.2.0.0. Both "Nd2File" and "Nd2ReadSdk" are needed.

Library functions:
    LIMFILEHANDLE(c_void_p) Lim_FileOpenForRead(LIMWCHAR)


"""

from ctypes import (c_int, c_uint32, c_uint64, c_float, c_char, c_char_p, 
    c_wchar, c_wchar_p, c_size_t, c_void_p, Structure, cdll, POINTER, c_uint)

from sys import platform
from pathlib import Path

#Load the required library files. Both "File" and "ReadSdk" files are needed.
basePath =  Path(__file__).parent / ".." / ".." / "lib"
if platform.startswith("win"):
    libPath = str((basePath / "win" / "Nd2File.dll").resolve())
    libPath2 = str((basePath / "win" / "Nd2ReadSdk.dll").resolve())
elif platform.startswith("linux"):
    libPath = str((basePath / "linux" / "Nd2File.so").resolve())
    libPath2 = str((basePath / "linux" / "Nd2ReadSdk.so").resolve())
elif platform.startswith("darwin"):
    libPath = str((basePath / "mac" / "Nd2File.dylib").resolve())
    libPath2 = str((basePath / "mac" / "Nd2ReadSdk.dylib").resolve())
else:
    pass

nd2File = cdll.LoadLibrary(libPath)
nd2Read = cdll.LoadLibrary(libPath2)

# Typedefs

LIMCHAR = c_char        # Multi-byte char for UTF-8 strings
LIMSTR = c_char_p       # Pointer to null-terminated multi-byte char array
LIMCSTR = c_char_p      # Pointer to null-terminated const multi-byte char

LIMWCHAR = c_wchar      # Wide-char (platform specific)
LIMWSTR = c_wchar_p     # Pointer to null-terminated wide-char array
LIMCWSTR = c_wchar_p    # Pointer to null-terminated const wide-char array

LIMUINT = c_uint32      # Unsigned integer 32-bit
LIMUINT64 = c_uint64    # Unsigned integer 64-bit
LIMSIZE = c_size_t      # Memory Size type
LIMINT = c_uint32       # Integer 32-bit
LIMBOOL = c_int         # Integer boolean value {0, 1}
LIMRESULT = c_int       # Integer boolean values

LIMFILEHANDLE = c_void_p    # Opaque type representing an opened ND2 file

# Definitions

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



# Function prototypes

# /*!
# \brief Opens an ND2 file for reading. This is widechar version.
# \param[in] wszFileName The filename (system wide-char) to be used.

# Returns \c nullptr if the file does not exist or cannot be opened for read or is corrupted.
# On succes returns (non-null) \c LIMFILEHANDLE which must be closed with \c Lim_FileClose to deallocate resources.
# \sa Lim_FileClose(), Lim_FileOpenForReadUtf8(LIMCSTR szFileNameUtf8)
# */

"""
# Lim_FileOpenForRead
#   Opens an ND2 file for reading. This is widechar version.
#
# Parameters:
#   wszFileName: The filename (system wide-char) to be used.
#
# Returns:
#   int (c nullptr): If file cannot be opened. Otherwise, returns a pointer to #   the file.
"""

Lim_FileOpenForRead = nd2Read.Lim_FileOpenForRead
Lim_FileOpenForRead.argtypes = [LIMCWSTR]
Lim_FileOpenForRead.restype = LIMFILEHANDLE

# /*!
# \brief Closes a file previously opened by this SDK.
# \param[in] hFile The handle to an opened file.

# If \a hFile is nullptr the function des nothing.

# \sa Lim_FileOpenForReadUtf8(LIMCSTR szFileNameUtf8), Lim_FileOpenForRead(LIMCWSTR wszFilename)
# */
Lim_FileClose = nd2Read.Lim_FileClose
Lim_FileClose.argtypes = [LIMFILEHANDLE]
Lim_FileClose.restype = None

# /*!
# \brief Opens an ND2 file for reading. This is multi-byte version (the encoding is utf-8).
# \param[in] szFileNameUtf8 The filename (multi-byte utf8 encoding) to be used.

# Returns \c nullptr if the file does not exist or cannot be opened for read or is corrupted.
# On succes returns (non-null) \c LIMFILEHANDLE which must be closed with \c Lim_FileClose to deallocate resources.
# \sa Lim_FileClose(), Lim_FileOpenForRead(LIMCWSTR wszFilename)
# */
Lim_FileOpenForReadUtf8 = nd2Read.Lim_FileOpenForReadUtf8
Lim_FileOpenForReadUtf8.argtypes = [LIMCSTR]
Lim_FileOpenForReadUtf8.restype = LIMFILEHANDLE

# /*!

# \brief Returs the dimensionality of the file or the number items in loop coordiante.
# \param[in] hFile The handle to an opened file.

# Zero means the file contains only one frame (not an ND document).
# */
Lim_FileGetCoordSize = nd2Read.Lim_FileGetCoordSize
Lim_FileGetCoordSize.argtypes = [LIMFILEHANDLE]
Lim_FileGetCoordSize.restype = LIMSIZE

# /*!
# \brief Returs size of the \a coord dimension.
# \param[in] hFile The handle to an opened file.
# \param[in] coord The index of the coordinate.
# \param[out] type Pointer to string buffer which receives the type.
# \param[in] maxTypeSize Maximum number of chars the buffer can hold.

# Coord must be lower than \c Lim_FileGetCoordSize().
# If \a type is not nullptr it is filled by the name of the loop type: "Unknown", "TimeLoop", "XYPosLoop", "ZStackLoop", "NETimeLoop".
# */
Lim_FileGetCoordInfo = nd2Read.Lim_FileGetCoordInfo
Lim_FileGetCoordInfo.argtypes = [LIMFILEHANDLE, LIMUINT, LIMSTR, LIMSIZE]
Lim_FileGetCoordInfo.restype = LIMUINT

# /*!
# \brief Returs the number of frames.
# \param[in] hFile The handle to an opened file.
# */
Lim_FileGetSeqCount = nd2Read.Lim_FileGetSeqCount
Lim_FileGetSeqCount.argtypes = [LIMFILEHANDLE]
Lim_FileGetSeqCount.restype = LIMUINT

# /*!
# \brief Converts coordinates into sequence index.
# \param[in] hFile The handle to an opened file.
# \param[in] coords The array of logical coordinates.
# \param[in] coordCount The number of logical coordinates.
# \param[out] seqIdx The pointer that is filled with corresponding sequence index.
#
# If wrong argument is passed or the coordinate is not present in the file the function fails and returns 0.
# On success it returns nonzero value.
# */
Lim_FileGetSeqIndexFromCoords = nd2Read.Lim_FileGetSeqIndexFromCoords
Lim_FileGetSeqIndexFromCoords.argtypes = [LIMFILEHANDLE, LIMUINT, LIMSIZE, LIMUINT]
Lim_FileGetSeqIndexFromCoords.restype = LIMBOOL

# /*!
# \brief Converts sequence index into coordinates.
# \param[in] hFile The handle to an opened file.
# \param[in] seqIdx The sequence index.
# \param[out] coords The array that is fileld with logical coordinates.
# \param[in] maxCoordCount The maximum nuber of coordinates the array can hold.

# On success it returns the number of coordinate dimensions.
# If coords is nullptr the function only returns the dimension of coordinate required to store the result.
# */
Lim_FileGetCoordsFromSeqIndex = nd2Read.Lim_FileGetCoordsFromSeqIndex
Lim_FileGetCoordsFromSeqIndex.argtypes = [LIMFILEHANDLE, LIMUINT, POINTER(LIMUINT * 4), LIMSIZE]
Lim_FileGetCoordsFromSeqIndex.restype = LIMSIZE

# Lim_FileGetAttributes
#   Returns attributes as JSON (object) string.
# 
# Parameters:
#   hFile: The handle to an opened file.
#
# Returns:
#   byteAttr: Attributes as a bytes object. Convert this to string using .decode()
#
# Attributes are always present in the file and contain following members:
#
# member                      | type               | description
# --------------------------- | ------------------ | ---------------
# bitsPerComponentInMemory    | number             | bits allocated to hold each component
# bitsPerComponentSignificant | number             | bits effectively used by each component (not used bits must be zero)
# componentCount              | number             | number of compoents in a pixel
# compressionLevel            | number, optional   | if comperssion is used the level of compression
# compressionType             | string, optional   | type of compression: "lossless" or "lossy"
# heightPx                    | number             | height of the image
# pixelDataType               | string             | undrlying data type "unsigned" or "float"
# sequenceCount               | number             | number of image frames in the file
# tileHeightPx                | number, optional   | suggested tile height if saved as tiled
# tileWidthPx                 | number, optional   | suggested tile width if saved as tiled
# widthBytes                  | number             | number of bytes from the beginning of one line to the next one
# widthPx                     | number             | width of the image
#
# The memory size for image buffer is calculated as widthBytes * heightPx.
#
# Returned string must be deleted using Lim_FileFreeString().

Lim_FileGetAttributes = nd2Read.Lim_FileGetAttributes
Lim_FileGetAttributes.argtypes = [LIMFILEHANDLE]
Lim_FileGetAttributes.restype = LIMSTR

# /*!
# \brief Returns metadata as JSON (object) string.
# \param[in] hFile The handle to an opened file.

# Presence of the metadata in the file as well as any field is optional.

# Metadata is broken per channel as it is the highest (most global)
# asset in the file. It contains only information which do not change per
# frame.

# These ate the metadata structures:

# structure    | where / different | description
# ------------ | ----------------- | ------------
# contents     | root (global)     | assets in the file (e.g. number of frames and channels)
# channels     | root (global)     | array of channels
# channel      | per channel       | channel related info (e.g. name, color)
# loops        | per channel       | loopname to loopindex map
# microscope   | per channel       | relevant microscope settings (magnifications)
# volume       | per channel       | image data valume related information

# _contents_ list number of assets:
# - channelCount determines the number of channels across all frames and
# - frameCount determines the number of frames in the file.

# _channels_ contais the array of channels where each contains:
# - channel
# - loops
# - microscope
# - volume

# _channel_ contains:
# - name of the channel,
# - index of the channel which uniquely identifies the channel in the file and
# - colorRGB definig the RGB color to show the channel in.

# _loops_ contains mapping from loop name into loopindex

# _microscope_ contains instrument related info:
# - objectiveName
# - objectiveMagnification
# - objectiveNumericalAperture
# - projectiveMagnification
# - zoomMagnification
# - immersionRefractiveIndex
# - pinholeDiameterUm

# _volume_ contains:
# - axesCalibrated contains 3 bools (XYZ) indicating which axes are calibrated
# - axesCalibration contains 3 doubles (XYZ) with calibration
# - axesInterpretation contains 3 strings (XYZ) defining the physical interpretation:
#    - distance (default) axis is in microns (um) and calibration is in um/px
#    - time axis is in milliseconds (ms) and calibration is in ms/px
# - bitsPerComponentInMemory
# - bitsPerComponentSignificant
# - componentCount
# - componentDataType is either unsigned or float
# - voxelCount contains 3 integers (XYZ) indicating the number of voxels in each direction
# - cameraTransformationMatrix a 2x2 matrix mapping camera space (origin is the image center, X going right, Y down) to normalized stage space (X going left, Y going up). It does not convert between pixels and um.
# - pixelToStageTransformationMatrix a 2x3 matrix which transforms pixel coordinates (origin is the image top-left corner) to the actual device coordinates in um. It does not add the image position to the coordinates.

# NIS Microscope Absolute frame in um = pixelToStageTransformationMatrix * (X_in_px  Y_in_px  1) + stagePositionUm

# Returned string must be deleted using Lim_FileFreeString().

# \sa Lim_FileFreeString()
# */
Lim_FileGetMetadata = nd2Read.Lim_FileGetMetadata
Lim_FileGetMetadata.argtypes = [LIMFILEHANDLE]
Lim_FileGetMetadata.restype = LIMSTR

# /*!
# \brief Returns frame metadata as JSON (object) string.
# \param[in] hFile The handle to an opened file.
# \param[in] uiSeqIndex The frame sequence index.

# Presence of the metadata in the file as well as any field is optional.

# By default (when metadataPointer is empty) the function returns all metadata
# updated with the current per-frame info.

# structure    | where / different       | description
# ------------ | ----------------------- | ------------
# position     | per frame and channel   | frame postion
# time         | per frame and channel   | frame time

# _position_ holds position of the frame
# - stagePositionUm contains 3 numbers (XYZ) indicating absolute position

# _time_ holds information anout the frame time
# - relativeTimeMs relative time (to the beginnig of the experiment) of the frame
# - absoluteJulianDayNumber absolute time of the frame (see https://en.wikipedia.org/wiki/Julian_day)
# - timerSourceHardware (if present) indicates the hardware used to capture the time (otherwise it is the software)

# In many cases it may be inefficient to retrieve all the data. In order to get only
# the data that change use the metadata pointer. E.g. in order to get only the time for the
# first channel call the function with `"/channels/0/time"`.

# Returned string must be deleted using Lim_FileFreeString().

# \sa Lim_FileFreeString()
# */

Lim_FileGetFrameMetadata = nd2Read.Lim_FileGetFrameMetadata
Lim_FileGetFrameMetadata.argtypes = [LIMFILEHANDLE, LIMUINT]
Lim_FileGetFrameMetadata.restype = LIMSTR

# /*!
# \brief Returns textinfo as JSON (object) string.
# \param[in] hFile The handle to an opened file.

# Presence of the textinfo in the file as well as any field is optional.

# Following fielads are available:
# - imageId
# - type
# - group
# - sampleId
# - author
# - description
# - capturing
# - sampling
# - location
# - date
# - conclusion
# - info1
# - info2
# - optics

# Returned string must be deleted using Lim_FileFreeString().

# \sa Lim_FileFreeString()
# */
Lim_FileGetTextinfo = nd2Read.Lim_FileGetTextinfo
Lim_FileGetTextinfo.argtypes = [LIMFILEHANDLE]
Lim_FileGetTextinfo.restype = LIMSTR

# /*!
# \brief Returns experiment as JSON (array) string.
# \param hFile The handle to an opened file.

# Presence of the experiment in the file as well as any field is optional.

# Experiment is an array of loop objects. Each loop object contains info about the loop.
# Each loop object contains:
# - type definig the loop type (either "TimeLoop", "XYPosLoop", "ZStackLoop", "NETimeLoop"),
# - count defining the number of iterations in the loop,
# - nestingLevel defining the loop level and
# - parameters describing the relevant experiment parameters.

# _TimeLoop_ contains following items in parameters:
# - startMs defining requested start of the sequence,
# - periodMs definig requested period,
# - durationMs defining requested duration and
# - periodDiff which contains frame-to-frane statistics (average, maximum and minimum).

# _NETimeLoop_ contains following items in parameters:
# - periods which is a array of period information where each item contains:
#    - count with the number of frames and
#    - startMs, periodMs, durationMs and periodDiff as in TimeLoop

# _XYPosLoop_ contains following items in parameters:
# - isSettingZ defines if th Z position was set when visiting each point (otherwise only XY was set) and
# - points which is an array of objects containing following members:
#    - stagePositionUm definig the position of the point,
#    - pfsOffset defining the pfs offset and
#    - name (optionally) contains the name of the point.

# _ZStackLoop_ contains following items in parameters:
# - homeIndex defines which index is home position,
# - stepUm defines the distance between slices
# - bottomToTop defines the acquisition direction
# - deviceName (optionally) contains the name of the device used to acquire the zStack.

# Returned string must be deleted using Lim_FileFreeString().

# \sa Lim_FileFreeString()
# */

Lim_FileGetExperiment = nd2Read.Lim_FileGetExperiment
Lim_FileGetExperiment.argtypes = [LIMFILEHANDLE]
Lim_FileGetExperiment.restype = LIMSTR

# /*!
# \brief Fills the \a pPicture with the frame indicated by the \a uiSeqIndex from the file.
# \param hFile The handle to an opened file.
# \param uiSeqIndex The the sequence index of the frame.
# \param pPicture The pointer to `LIMPICTURE` structure that is filled with picture data.

# If the \a pPicture is nullptr the function fails.

# If the \c LIMPICTURE::pImageData and \c LIMPICTURE::uiSize members are zero the \c LIMPICTURE is properly initialized using to \c Lim_InitPicture.

# If the \a pPicture is already initialized but the size doesnt match the function fails.

# The \a pPicture must be deleted using Lim_DestroyPicture().

# \sa Lim_InitPicture(), Lim_DestroyPicture()
# */
Lim_FileGetImageData = nd2Read.Lim_FileGetImageData
Lim_FileGetImageData.argtypes = [LIMFILEHANDLE, LIMUINT, POINTER(LIMPICTURE)]
Lim_FileGetImageData.restype = LIMRESULT

# /*!
# \brief Deallocates the string returned by metadata retrieving SDK function.
# \param str The pointer to the string to be deallocated.

# \sa Lim_FileGetAttributes(), Lim_FileGetExperiment(), Lim_FileGetMetadata(), Lim_FileGetFrameMetadata(), Lim_FileGetTextinfo()
# */
Lim_FileFreeString = nd2Read.Lim_FileFreeString
Lim_FileFreeString.argtypes = [LIMSTR]
Lim_FileFreeString.restype = None

# /*!
# \brief Initializes and allocates \a pPicture buffer to hold the image with given parameters.
# \param pPicture The pointer `LIMPICTURE` structure to be initialized.
# \param width The width (in pixels) of the picture.
# \param height The height (in pixels) of the picture.
# \param bpc The number of bits per each component (integer: 8-16 and floating: 32).
# \param components The number of components in each pixel.

# The parameters \a width, \a height \a bpc (bits per component) and \a components (number of color components in each pixel) are taken from attributes (Lim_FileGetAttributes()).

# \sa Lim_DestroyPicture()
# */
Lim_InitPicture = nd2Read.Lim_InitPicture
Lim_InitPicture.argtypes = [POINTER(LIMPICTURE), LIMUINT, LIMUINT, LIMUINT, LIMUINT]
Lim_InitPicture.restype = LIMSIZE

# /*!
# \brief Deallocates resources allocated by \c Lim_InitPicture().
# \param pPicture The pointer `LIMPICTURE` structure to be deallocated.
#
# \sa Lim_InitPicture()
# */
Lim_DestroyPicture = nd2Read.Lim_DestroyPicture
Lim_DestroyPicture.argtypes = [POINTER(LIMPICTURE)]
Lim_DestroyPicture.restype = None