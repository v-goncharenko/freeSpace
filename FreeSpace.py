import numpy as np
from scipy.constants import speed_of_light as c

class FreeSpace(object):
	"""
	Implements signal proragation in free space.
	Accounts in calculations:
		* time delay
		* doppler effect
		* signall loss

	Attributes:
		propagation_speed: 
		operating_frequency: 
		sample_rate: 
	"""
	def __init__(self, propagation_speed=c, operating_frequency, sample_rate):
		super(FreeSpace, self).__init__()
		self.arg = arg

	def step(self):
		pass
