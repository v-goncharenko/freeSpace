import unittest
import numpy.testing as nptest
from scipy import io
import numpy as np
import logging

import generate_tests
import test_matlab
import test_free_space

logging.basicConfig(level=logging.DEBUG)

class CompareTests(unittest.TestCase):
    def test_compare(self):
        for test in generate_tests.tests:
            print('test #{} runs'.format(test))

            # extract matlab
            matlab_res = io.loadmat('{}{}_{}'.format(generate_tests.tests_path, test, 'matlab'))
            matlab = np.array(matlab_res[test_matlab.MatlabTest.save_name], copy=False)
            logging.debug('matlab: {}'.format(matlab_res[test_matlab.MatlabTest.save_name][:10]))

            # extract FreeSpace
            python_res = io.loadmat('{}{}_{}'.format(generate_tests.tests_path, test, 'python'))
            python = np.array(python_res[test_free_space.FreeSpaceTest.save_name], copy=False)
            logging.debug('pyton: {}'.format(python_res[test_free_space.FreeSpaceTest.save_name][:10]))

            nptest.assert_allclose(python, matlab, err_msg='test #{} failed'.format(test))

            print('run succesfully!')

    # def test_compare_double_input(self):
    #     test = '4'
    #     print('test #{} runs'.format(test))

    #     # extract matlab
    #     matlab_res = io.loadmat('{}{}_{}'.format(generate_tests.tests_path, test, 'matlab'))
    #     matlab_1 = np.array(matlab_res[test_matlab.MatlabTest.save_name + '_1'], copy=False)
    #     logging.debug('matlab_1: {}'.format(matlab_1[:10]))
    #     matlab_2 = np.array(matlab_res[test_matlab.MatlabTest.save_name + '_2'], copy=False)
    #     logging.debug('matlab_2: {}'.format(matlab_2[:10]))


    #     # extract FreeSpace
    #     python_res = io.loadmat('{}{}_{}'.format(generate_tests.tests_path, test, 'python'))
    #     python_1 = np.array(python_res[test_free_space.FreeSpaceTest.save_name + '_1'], copy=False)
    #     logging.debug('pyton_1: {}'.format(python_1[:10]))
    #     python_2 = np.array(python_res[test_free_space.FreeSpaceTest.save_name + '_2'], copy=False)
    #     logging.debug('pyton_2: {}'.format(python_2[:10]))

    #     nptest.assert_allclose(python_1, matlab_1)
    #     nptest.assert_allclose(python_2, matlab_2)

if __name__ == '__main__':
    unittest.main()
 