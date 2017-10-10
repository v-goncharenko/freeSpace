import unittest
import numpy.testing as nptest
from scipy import io
import numpy as np

import generate_tests
from test_matlab import MatlabTest
from test_free_space import FreeSpaceTest

class CompareTests(unittest.TestCase):
    def compare_tests
    for test in tests:
        matlab = io.loadmat('{}{}_{}'.format(tests_path, test, 'matlab'))

        ans = np.array(matlab[matlab_save_name], copy=False)
        print(ans)
        print('##', ans.shape)
        for el in ans:
            print(el, type(el), el.shape)
        print('%%%')
        print(ans[0])

if __name__ == '__main__':
    unittest.main()
