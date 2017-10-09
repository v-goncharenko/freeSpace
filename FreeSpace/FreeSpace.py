import numpy as np
import math
import itertools as it
from scipy import constants as consts
import logging

logging.basicConfig(level=logging.DEBUG)

class FreeSpace(object):
    """
    Implements signal proragation in free space.
    Accounts in calculations:
        * time delay
        * doppler effect
        * signal loss
    """
    def __init__(self,
                 propagation_speed=consts.c,
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

    def __str__(self):
        return 'FreeSpace object'

    def step(self, signal, origin_pos, dest_pos, origin_vel, dest_vel):
        """
        Performs signal propagation in space configured.
        :param array-like signal: (maybe complex) amplitude of transmitted signal
        :param array-like origin_pos: position of signal origin in 3-d space
        :param array-like dest_pos: signal destination, see origin_pos
        :param array-like origin_vel: origin velocity, see origin_pos
        :param array-like dest_vel: destination velocity see origin_pos
        :returns array-like: received signal
        """
        # premutate all input to np array form
        signal = FreeSpace._prepare_vector(signal)
        logging.debug('signal head: {}'.format(signal[:5]))
        logging.debug('signal.shape: {}'.format(signal.shape))
        origin_pos = FreeSpace._prepare_vector(origin_pos)
        dest_pos = FreeSpace._prepare_vector(dest_pos)
        origin_vel = FreeSpace._prepare_vector(origin_vel)
        dest_vel = FreeSpace._prepare_vector(dest_vel)

        received = np.empty_like(signal, dtype=np.complex_)

        conditions = self._conditions(origin_pos, dest_pos, origin_vel, dest_vel, signal.size)
        for moment, time, distance in conditions:
            # tau is time shift between signal emmision and reception
            tau = distance / self.propagation_speed
            logging.debug(' @@@ moment: {}, time: {}, distance: {}'.format(moment, time, distance))
            if tau > time:
                received[moment] = 0
            else:
                # TODO how to round values?
                emission_moment = moment - int(tau * self.sample_rate)
                original_signal = signal[emission_moment]
                logging.debug('original_signal {}'.format(original_signal))
                received[moment] = original_signal * self._loss(tau) * self._phase_shift(tau)
        return received

    @staticmethod
    def _prepare_vector(object, size=None):
        """
        Makes vector (1 dimentional array) out of object if it's possible, else throws an exception
        :param array-like object: numpy-compatible object (could be agregated by np.array)
        :param integer or None size: number of components that vector has in it's only dimention
        :returns array-like: 1 dimentional numpy array made from object
        """
        vector = np.array(object, copy=False)
        vector = np.squeeze(vector)
        if vector.ndim != 1:
            raise ValueError('Inputed vector must be one dimentional!')
        if size and vector.shape[0] != size:
            raise ValueError('This vector must have {} components'.format(size))
        return vector

    def _conditions(self, origin_pos, dest_pos, origin_vel, dest_vel, to_moment):
        """
        This function returns generator that yields values of time and distance
        between origin and destination in scale of sample_rate. This means that
        first distance is initial, second is in time 1/sample_rate, third:
        2/sample_rate and so on
        :param integer to_moment: moment to generate conditions to
        """
        # change coordinate system to origin's
        init_pos = dest_pos - origin_pos
        relative_vel = dest_vel - origin_vel

        # moments will be measured in scale of sample_rate
        # time beween two nearby moments is
        sample_time_increment = 1 / self.sample_rate
        # count of how many tics passed
        moment_counter = it.count()
        moment = next(moment_counter)

        while moment < to_moment:
            time = moment * sample_time_increment
            position = init_pos + relative_vel * time
            yield moment, time, np.linalg.norm(position)
            moment = next(moment_counter)

    def _loss(self, tau):
        loss = np.power(4 * consts.pi * tau * self.operating_frequency, -1)
        logging.debug('loss: {}, dtype: {}'.format(loss, loss.dtype))
        return np.squeeze(loss)

    def _phase_shift(self, tau):
        shift = np.exp(-1j * 2 * consts.pi * self.operating_frequency * tau)
        logging.debug('phase shift: {}, dtype: {}'.format(shift, shift.dtype))
        return np.squeeze(shift)
