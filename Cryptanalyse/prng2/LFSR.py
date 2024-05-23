class LFSR:

	def __init__(self, fpoly=None, state=None):
		self.state = state
		self.fpoly = fpoly
		self.out = None
		if fpoly is not None and len(fpoly)<2:
			Exception("Polynomial function must contain at least 2 not null coefficients")

	def _compute_feedback(self):
		output = self.state[self.fpoly[0]-1]^self.state[self.fpoly[1]-1]
		for i in range(2,len(self.fpoly)):
			output^=self.state[self.fpoly[i]-1]
		return output

	def _update_state(self,feedback):
		self.out = self.state[-1]
		self.state = [feedback]+self.state[:-1]

	def _next_state(self):
		if self.state is None:
			raise Exception("State must be not None")
		if self.fpoly is None:
			raise Exception("Polynomial function must be not None")

		feedback = self._compute_feedback()
		self._update_state(feedback)

	def generateBit(self):
		self._next_state()
		return self.out

	def generateByte(self):
		byte = 0
		for i in range(8):
			self._next_state()
			byte += int(self.out)*2**(7-i)
		return byte.to_bytes(length=1,byteorder='big')

	def generateBytes(self,size):
		bytes_out = b''
		for i in range(size):
			bytes_out+=self.generateByte()
		return bytes_out

	def copy(self):
		return LFSR(fpoly=self.fpoly.copy(),state=self.state.copy())