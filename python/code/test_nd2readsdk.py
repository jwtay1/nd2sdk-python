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

        print(expmd.uiLevelCount)

        print(expmd.pAllocatedLevels[0].uiExpType)
        print(expmd.pAllocatedLevels[1].uiExpType)
        print(expmd.pAllocatedLevels[2].uiExpType)
        print(expmd.pAllocatedLevels[3].uiExpType)

        print("------\n")
        print(expmd.pAllocatedLevels[0].uiLoopSize)
        print(expmd.pAllocatedLevels[0].dInterval)

        print("------\n")
        print(expmd.pAllocatedLevels[1].uiLoopSize)
        print(expmd.pAllocatedLevels[1].dInterval)

        print("------\n")
        print(expmd.pAllocatedLevels[2].uiLoopSize)
        print(expmd.pAllocatedLevels[2].dInterval)




# import os

# dlldir = os.path.join(os.path.dirname(__file__), "..", "..", 'lib', 'win')
# os.environ["PATH"] += os.pathsep + os.path.join(dlldir)

# import nd2ReadSDK as nd2
# from pathlib import Path

# import numpy as np
# from matplotlib import pyplot as plt
# import ctypes

# testFP = Path("D:\\Jian\\Documents\\Projects\\myprojects\\ND2SDK\\nd2sdk-wrappers\\sampleND2\\sampleND2.nd2")

# _fh = nd2.Lim_FileOpenForRead(str(testFP.resolve()))

# attr = nd2.LIMATTRIBUTES()

# res = nd2.Lim_FileGetAttributes(_fh, attr)
# print(res)

# md = nd2.LIMMETADATA_DESC()
# res = nd2.Lim_FileGetMetadata(_fh, md)
# print(res)

# _buf_pic = nd2.LIMPICTURE()
# res = nd2.Lim_InitPicture(_buf_pic, attr.uiWidth, attr.uiHeight, attr.uiBpcSignificant, attr.uiComp)
# print(res)

# localMD = nd2.LIMLOCALMETADATA()
# res = nd2.Lim_FileGetImageData(_fh, 0, _buf_pic, localMD)
# print(res)

# _array_pic = ctypes.c_uint16 * attr.uiWidth * attr.uiHeight * attr.uiComp
# _array_pic_p = _array_pic.from_address(_buf_pic.pImageData)

# im = np.ndarray((attr.uiHeight, attr.uiWidth, attr.uiComp),
#                 np.uint16, _array_pic_p).copy()

# plt.imshow(im[:,:,0])
# plt.show()


# nd2.Lim_DestroyPicture(_buf_pic)

# res = nd2.Lim_FileClose(_fh)
# print(res)


if __name__ == '__main__':
    unittest.main()