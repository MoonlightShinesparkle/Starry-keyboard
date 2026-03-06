import time
import busio

class Mem24LC16:
	def __init__(self, i2c : busio.I2C, Address : int = 0x50):
		self.i2c = i2c
		self.BaseAddress = Address
		self.Length = 2048
		self.BlockSize = 256
		self.SingleBytebuffer = bytearray(1)

	def ParseAddress(self, Target):
		"""Parses a target point into an 24LC16 useable address"""

		# Gets target block (0 -> 7)
		Address = Target // self.BlockSize

		# Gets the offset within the block (0 -> 255)
		Offset = Target % self.BlockSize

		# Return 0x5<Address> & Offset
		return self.BaseAddress+Address, Offset
	
	def __len__(self):
		return self.Length
	
	def _LockI2C(self):
		while not self.i2c.try_lock():
			pass
	
	def __getitem__(self, key):
		# Check if the key is a slice
		if isinstance(key,slice):
			# Begins at given start or just 0
			Start = key.start or 0

			# Ends at given end or just read the whole thing alltogether
			End = key.stop or self.Length

			# Create buffer to store data into
			Buffer = bytearray(End-Start)
			# Populate buffer
			for x in range(len(Buffer)):
				Buffer[x] = self[Start+x] # Ask itself for data... with a non-slice
			# Return the populated buffer
			return Buffer
		
		# It is not a slice, use number
		Address, Offset = self.ParseAddress(key)

		# Lock I2C bus
		self._LockI2C()

		try:
			# Acquire data
			self.i2c.writeto_then_readfrom(Address,bytes([Offset]),self.SingleBytebuffer)
		finally:
			# Release I2C bus
			self.i2c.unlock()

		return self.SingleBytebuffer[0]
	
	def __setitem__(self, key, value):
		if isinstance(key,slice):
			Start = key.start or 0
			End = key.stop or self.Length

			for x in range(End-Start):
				self[Start+x] = value[x] or 0

		Address, Offset = self.ParseAddress(key)

		# Lock I2C bus
		self._LockI2C()

		try:
			# Write data
			self.i2c.writeto(Address,bytes([Offset,value]))
		finally:
			# Release I2C bus
			self.i2c.unlock()

		time.sleep(0.005)