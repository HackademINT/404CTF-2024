from LFSR import LFSR
class CombinerGenerator:
	def __init__(self,function,*LFSRs):
		self.function = function
		self.LFSRs = LFSRs
		self.LFSRs_init = tuple([lfsr.copy() for lfsr in self.LFSRs])

	def _compute_out(self):
		if self.function is None:
			raise Exception("Function must be not None")
		if self.LFSRs is None:
			raise Exception("No LFSR given")
		for lfsr in self.LFSRs:
			if lfsr.state is None:
				raise Exception("LFSR state must be initialized")

		lfsrs_output = []
		for lfsr in self.LFSRs:
			lfsrs_output.append(lfsr.generateBit())
		self.out = self.function(*lfsrs_output)

	def generateBit(self):
		self._compute_out()
		return self.out

	def generateByte(self):
		byte = 0
		for i in range(8):
			self._compute_out()
			byte += int(self.out)*2**(7-i)
		return byte.to_bytes(length = 1,byteorder='big')