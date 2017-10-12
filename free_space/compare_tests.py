import unittest
import numpy.testing as nptest
from scipy import io
import numpy as np

import generate_tests
import test_matlab
import test_free_space

class CompareTests(unittest.TestCase):
    def test_compare(self):
        for test in generate_tests.tests:
            print('test #{} runs'.format(test))

            # extract matlab
            matlab_res = io.loadmat('{}{}_{}'.format(generate_tests.tests_path, test, 'matlab'))
            matlab = np.array(matlab_res[test_matlab.MatlabTest.save_name], copy=False)

            # extract FreeSpace
            python_res = io.loadmat('{}{}_{}'.format(generate_tests.tests_path, test, 'python'))
            python = np.array(python_res[test_free_space.FreeSpaceTest.save_name], copy=False)

            nptest.assert_allclose(python, matlab)

if __name__ == '__main__':
    unittest.main()
