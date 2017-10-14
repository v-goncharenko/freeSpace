import unittest
from scipy import io

import free_space
import generate_tests

class FreeSpaceTest(unittest.TestCase):
    save_name = 'received'

    def test_mat_files(self):
        for test in generate_tests.tests:
            print('test #{}\n'.format(test))

            # read input from mat file
            input_dict = io.loadmat('{}{}_{}'.format(generate_tests.tests_path, test, 'input'))

            # perform tests
            fs = free_space.FreeSpace(**{ label: input_dict[label] for label in generate_tests.fs_labels})
            received = fs.step(**{label: input_dict[label] for label in generate_tests.step_labels})

            print(received.shape)

            # write results to mat file
            io.savemat('{}{}_python'.format(generate_tests.tests_path, test),
                       {self.save_name: received[:, None]})

    # def test_multiple_input(self):
    #         test = '4'
    #         print('test #{}\n'.format(test))

    #         # read input from mat file
    #         input_dict = io.loadmat('{}{}_{}'.format(generate_tests.tests_path, test, 'input'))

    #         # perform tests
    #         fs = free_space.FreeSpace(**{ label: input_dict[label] for label in generate_tests.fs_labels})

    #         received_1 = fs.step(**{label: input_dict[label] for label in generate_tests.step_labels})

    #         print(received.shape)

    #         # write results to mat file
    #         io.savemat('{}{}_python'.format(generate_tests.tests_path, test),
    #                    {self.save_name: received[:, None]})


if __name__ == '__main__':
    unittest.main()
