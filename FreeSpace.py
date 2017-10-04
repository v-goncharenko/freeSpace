import numpy as np
from scipy.constants import speed_of_light as c

class FreeSpace(object):
    """
    Implements signal proragation in free space.
    Accounts in calculations:
        * time delay
        * doppler effect
        * signall loss
    """
    def __init__(self,
                 propagation_speed=c,
                 operating_frequency=3e8,
                 sample_rate=1e6,
                 two_way_propagation=False):
        """
        Cnostructs ready to use FreeSpace object.
        :param number propagation_speed: speed of signal propagation in this space, default is speed of light
        :param number operating_frequency: 
        :param number sample_rate: 
        :param bool two_way_propagation: return signal transmitted either from origin to dest (if set to False)
            or in both directinos
        """
        super(FreeSpace, self).__init__()
        self.propagation_speed = propagation_speed
        self.operating_frequency = operating_frequency
        self.sample_rate = sample_rate
        self.two_way_propagation = two_way_propagation

    def step(self, signal, origin_pos, dest_pos, origin_vel, dest_vel):
        _check_input(origin_pos, dest_pos, origin_vel, dest_vel)
        

    def _check_input(self):
        pass