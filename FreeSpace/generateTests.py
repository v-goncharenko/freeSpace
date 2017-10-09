from scipy import io

fs_labels = [
    'operating_frequency',
    'sample_rate',
]
step_labels = [
    'signal',
    'origin_pos',
    'dest_pos',
    'origin_vel',
    'dest_vel',
]

def gen_simple_test():
    """
    #1
    The most simple test from phased.FreeSpace docs
    """
    count = 1
    mdict = {
        'operating_frequency':  3e8,
        'sample_rate':          8e3,
        'signal':               [1] * 5,
        'origin_pos':           [1000, 0, 0],
        'dest_pos':             [300, 200, 50],
        'origin_vel':           [0] * 3,
        'dest_vel':             [0] * 3,
    }
    io.savemat('testCases/{}_input'.format(count), mdict)

if __name__ == '__main__':
    gen_simple_test()
    print('ok =)')
