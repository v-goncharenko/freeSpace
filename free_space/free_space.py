import numpy as np
import itertools as it
from scipy import constants as consts
import math
import logging

# logging.basicConfig(level=logging.DEBUG)

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
        self._propagation_ratio = 2.0 if two_way_propagation else 1.0

    def __str__(self):
        return 'FreeSpace object'

    def __repr__(self):
        return ('FreeSpace with propagation speed {}, operating frequency {},'
                'sample rate {}, propagation ratio {}').format(self.propagation_speed,
                    self.operating_frequency, self.sample_rate, self._propagation_ratio)

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
        signal = FreeSpace._prepare_vector(signal, dtype=np.complex_)
        logging.debug('signal head: {}'.format(signal[:5]))
        logging.debug('signal.shape: {}'.format(signal.shape))
        origin_pos = FreeSpace._prepare_vector(origin_pos, 3)
        dest_pos = FreeSpace._prepare_vector(dest_pos, 3)
        origin_vel = FreeSpace._prepare_vector(origin_vel, 3)
        dest_vel = FreeSpace._prepare_vector(dest_vel, 3)

        # allocate space for result
        received = np.empty_like(signal, dtype=np.complex_)

        # precalculate support values
        relative_pos = dest_pos - origin_pos
        relative_vel = dest_vel - origin_vel
        distance = np.squeeze(np.linalg.norm(relative_pos))
        # tau is time shift between signal emission and reception
        tau = self._propagation_ratio * distance / self.propagation_speed
        logging.debug('tau: {}'.format(tau))
        loss = self._loss(tau)
        phase_shift = self._phase_shift(tau)
        delay_frac, delay_int = math.modf(tau * self.sample_rate)
        delay_int = int(delay_int)
        doppler_shift = self._doppler_shift(tau, relative_pos, relative_vel, delay_int)
        # delay signal to delay_int moments, but keep overall length
        delayed_signal = it.islice(
            it.chain(it.repeat(0, delay_int), signal),
            signal.size
        )

        # to compute interpolated signal we need signal value at previous moment
        prev_signal = 0
        for moment, curr_signal in enumerate(delayed_signal):
            curr_signal = curr_signal * loss * phase_shift * doppler_shift(moment)
            interpolated = prev_signal * delay_frac + curr_signal * (1 - delay_frac)
            received[moment] = interpolated
            prev_signal = curr_signal

        logging.debug('received head {}'.format(received[:10]))
        return received

    @staticmethod
    def _prepare_vector(object, size=None, dtype=np.float_):
        """
        Makes vector (1 dimentional array) out of object if it's possible, else throws an exception
        :param array-like object: numpy-compatible object (could be agregated by np.array)
        :param integer or None size: number of components that vector has in it's only dimention
        :param data-type dtype: data type used to construct numpy array, see np.array
        :returns array-like: 1 dimentional numpy array (shaped (n, )) made from object
        """
        vector = np.array(object, copy=False, dtype=dtype)
        vector = np.squeeze(vector)
        if vector.ndim != 1:
            raise ValueError('Inputed vector must be one dimentional!')
        if size and vector.size != size:
            raise ValueError('This vector must have {} components'.format(size))
        return vector

    def _loss(self, tau):
        loss = np.power(4 * consts.pi * tau * self.operating_frequency, -1)
        logging.debug('inverted loss: {}, dtype: {}'.format(1 / loss, loss.dtype))
        return np.squeeze(loss)

    def _phase_shift(self, tau):
        shift = np.exp(-1j * 2 * consts.pi * self.operating_frequency * tau)
        logging.debug('phase shift: {}, dtype: {}'.format(shift, shift.dtype))
        return np.squeeze(shift)

    def _doppler_shift(self, tau, relative_pos, relative_vel, delay_int):
        """
        Returns lambda which depends on moment.
        Moment counts from beginning of received signal, but due to Matlab's
        implementation, **doppler's addition counts from delay_int**
        Also we could use negative indexes since signal for thoose indexes is
        always zero
        """
        vel_projection = - np.dot(relative_vel, relative_pos) / np.linalg.norm(relative_pos)
        logging.debug('vel_projection: {}'.format(vel_projection))
        coef = ( 1j * 2 * consts.pi * self._propagation_ratio * vel_projection
            * self.operating_frequency / self.propagation_speed )
        # init_shift = np.exp(coef * tau)
        # shift_increment = np.exp(coef / self.sample_rate)
        return lambda moment: np.squeeze( np.exp(
            coef * (tau + (moment - delay_int) / self.sample_rate)
        ) )
