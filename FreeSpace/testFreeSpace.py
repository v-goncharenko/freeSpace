import unittest
import numpy.testing as nptest
import FreeSpace
from scipy import io
import numpy as np

import generateTests

class FreeSpaceTest(unittest.TestCase):
    tests = ['1']
    tests_path = 'testCases/'

    def test_create_instance(self):
        fs = FreeSpace.FreeSpace()

    def test_mat_files(self):
        for test in self.tests:
            input_dict = io.loadmat('{}{}_{}'.format(self.tests_path, test, 'input'))
            fs = FreeSpace.FreeSpace(**{ label: input_dict[label] for label in generateTests.fs_labels})
            received = fs.step(**{label: input_dict[label] for label in generateTests.step_labels})
            print(' $#@ received:')
            for val in received * 1e5:
                print(val)
            # for key, value in input_dict.items():
            #     print('# key: ', key)
            #     print('$ value type: ', type(value))
            #     print('@ value: ', value)
            # ans = np.array(matlab[matlab_variable_name], copy=False)
            

if __name__ == '__main__':
    unittest.main()