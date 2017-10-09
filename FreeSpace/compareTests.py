from scipy import io
import numpy as np

tests = ['1']
tests_path = 'testCases/'
matlab_variable_name = 'y'

for test in tests:
    matlab = io.loadmat('{}{}_{}'.format(tests_path, test, 'matlab'))

    ans = np.array(matlab[matlab_variable_name], copy=False)
    print(ans)
    print('##', ans.shape)
    for el in ans:
        # el[0] = 122
        print(el, type(el), el.shape)
    # print(ans)
    print('%%%')
    print(ans[0])
