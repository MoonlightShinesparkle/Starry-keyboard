import board
import busio
import random
import time
import Mem24lc16

i2c : busio.I2C = busio.I2C(board.GP11,board.GP10)

EEProm : Mem24lc16.Mem24LC16 = Mem24lc16.Mem24LC16(i2c)

def PrintLen():
	print(f"Initialized with EEPROM length of {len(EEProm)}")

def TestWrite():
	print(f"Currently stored data in EEPROM: {EEProm[0:4]}")
	for x in range(4):
		val : int = random.randint(0,10)
		EEProm[x] = val
		print(f"Wrote {val} into {x}")
		time.sleep(0.006)
	print(f"New stored data in EEPROM: {EEProm[0:4]}")
	for x in range(4):
		print(f"{EEProm[x]}")
