# Free Space
Implements signal proragation in free space.
Inspiered by Matlab's [phased.FreeSpace](https://www.mathworks.com/help/phased/ref/phased.freespace-system-object.html?s_tid=gn_loc_drop) and tested to have the same results.
Accounts in calculations:
* time delay
* doppler effect
* signal loss

## Assumptions
* Propagation speed > origin velocity
* Propagation speed > destination velocity
* Initial distance >> relative velocity * broadcast time

## Test suite
**generateTests.m** - код на матлабе для генерации тестов

**generateTests.py** - generates a set of tests with different parameters (random or predefined), saves it in .mat file (and maybe .pickle file for Python)
Outputs:
    <!-- * propagation_speed -->
    * operating_frequency
    * sample_rate
    * two_way_propagation
    * signal
    * origin_pos
    * dest_pos
    * origin_vel
    * dest_vel

**testMatlab.py** - runs existing tests (reads form .mat files) in Matlab by [Matlab API for Python](https://www.mathworks.com/help/matlab/matlab-engine-for-python.html) and saves results (to .mat or .picle). Internally runs matlab function.
Outputs:
    * y

**testFreeSpace.py** - runs existing tests in FreeSpace and saves results (or compares with Matlab's?)

**compareTests.py** - checks if Matlab's and Python's results are equal

## Enviroment
Project uses Python 3.5.4 (it pointed in .python-version file)
Python requirements for using this code listed in `requirements.txt`, also development requirements listed in `dev-requirements.txt`

Matlab version is R2016b (9.1), 64-bit(glnxa64)

## Code style
We use [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
except line length set to 120.