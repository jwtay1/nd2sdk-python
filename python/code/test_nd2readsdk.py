import unittest
from pathlib import Path
import nd2ReadSDK as nd2api
import ctypes
import numpy as np
from matplotlib import pyplot as plt

class TestND2ReadSDK(unittest.TestCase):

    #Path to test file
    path_testfile =  Path("D:\\Jian\\Documents\\Projects\\myprojects\\ND2SDK\\nd2sdk-wrappers\\sampleND2\\sampleND2.nd2")

    #Expected results    
    uiWidth = 276
    uiLevelCount = 2

    def setUp(self):
        self._fh = nd2api.Lim_FileOpenForRead(str(self.path_testfile))
    
    def tearDown(self):
        result = nd2api.Lim_FileClose(self._fh)

    def test_Lim_FileGetAttributes(self):

        attr = nd2api.Lim_FileGetAttributes(self._fh)

        self.assertEqual(attr.uiWidth, self.uiWidth)
    
    def test_Lim_FileGetMetadata(self):

        md = nd2api.Lim_FileGetMetadata(self._fh)

        self.assertTrue(md.dTimeStart != 0)

    def test_nofile_Lim_FileOpenForRead(self):
        
        self.assertRaises(FileNotFoundError, nd2api.Lim_FileOpenForRead, "not_a_file.nd2")

    def test_retrieve_image(self):
        #Note: This is somewhat difficult to test so I'm relying on internal errors to show that the test is completed. In other words, assume that the image returned is correct if the functions below do not raise an exception.

        #Get required image attributes
        imgAttr = nd2api.Lim_FileGetAttributes(self._fh)
        
        #Initialize the picture buffer
        pic_buffer = nd2api.Lim_InitPicture(imgAttr.uiWidth, imgAttr.uiHeight, 
                                            imgAttr.uiBpcSignificant, 
                                            imgAttr.uiComp)
        
        #Populate image data
        pic_md = nd2api.Lim_FileGetImageData(self._fh, 0, pic_buffer)

        #Create a new ctypes instance using the memory address returned
        uint_array = ctypes.c_uint16 * imgAttr.uiWidth * imgAttr.uiHeight *                  imgAttr.uiComp
        pic_data = uint_array.from_address(pic_buffer.pImageData)

        im = np.ndarray((imgAttr.uiHeight, imgAttr.uiWidth, imgAttr.uiComp),
                 np.uint16, pic_data).copy()

        #plt.imshow(im[:,:,0])
        #plt.show()

    def test_Lim_FileGetExperiment(self):

        expmd = nd2api.Lim_FileGetExperiment(self._fh)

        self.assertEqual(expmd.uiLevelCount, self.uiLevelCount)

    def test_Lim_GetSeqIndexFromCoords_fhandle(self):

        seq_index = nd2api.Lim_GetSeqIndexFromCoords(self._fh, 
                                                    4, 0, 0, 0)

        self.assertGreaterEqual(seq_index, 0)

    def test_Lim_GetSeqIndexFromCoords_expmd(self):

        expmd = nd2api.Lim_FileGetExperiment(self._fh)

        seq_index = nd2api.Lim_GetSeqIndexFromCoords(expmd, 
                                                    4, 0)
        self.assertGreaterEqual(seq_index, 0)

    def test_Lim_GetSeqIndexFromCoords_indexTooLarge(self):

        self.assertRaises(ValueError,
                          nd2api.Lim_GetSeqIndexFromCoords,
                          self._fh, 9, 2)

    def test_Lim_FileGetBinaryDescriptors(self):

        binaries = nd2api.Lim_FileGetBinaryDescriptors(self._fh)
        print(binaries.uiCount)



if __name__ == '__main__':
    unittest.main()
    