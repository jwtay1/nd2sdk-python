#Test code for the ND2 SDK Python wrapper
#
#Test memory leak - tracemalloc (https://docs.python.org/3/library/tracemalloc.html)

import unittest
from nd2reader import ND2reader

class TestND2reader(unittest.TestCase):
    
    def main(self):
        """ Run tests



        """

        #Put calls to the tests to run here
        self.testConstruct()
        
        pass

    def testConstruct(self):
        R = ND2reader("D:\\Jian\\Documents\\Projects\\myprojects\\ND2SDK\\nd2sdk-wrappers\\sampleND2\\sampleND2.nd2")

        R.getImage(1)

if __name__ == '__main__':
    unittest.main()
