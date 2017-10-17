import unittest
import time
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
            start = time.perf_counter()
            received = fs.step(**{label: input_dict[label] for label in generate_tests.step_labels})
            end = time.perf_counter()
            print('took {:f} seconds'.format(end - start))

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

    #         labels = {label: input_dict[label] for label in generate_tests.step_labels if label != 'signal'}
    #         labels['signal'] = input_dict['signal_1']
    #         received_1 = fs.step(**labels)

    #         labels['signal'] = input_dict['signal_2']
    #         received_2 = fs.step(**labels)

    #         # write results to mat file
    #         io.savemat('{}{}_python'.format(generate_tests.tests_path, test),
    #                    {self.save_name + '_1': received_1[:, None],
    #                     self.save_name + '_2': received_2[:, None] })

if __name__ == '__main__':
    unittest.main()
