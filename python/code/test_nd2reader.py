import unittest
from nd2reader import ND2reader
from pathlib import Path
from matplotlib import pyplot as plt

class TestND2Reader(unittest.TestCase):

    test_file = Path(__file__) / ".." / ".." / ".." / "sampleND2" / "sampleND2.nd2"

    def setUp(self):
        self.reader = ND2reader(str(self.test_file.resolve()))

    def test_getImage_byIndex(self):

        im = self.reader.getImage(0)
        
        plt.imshow(im[:,:,0])
        plt.show()

    def test_getImage_byCoords(self):

        im = self.reader.getImage(3, 0, 0, 0)
        
        plt.imshow(im[:,:,0])
        plt.show()

        


if __name__ == "__main__":
    unittest.main()