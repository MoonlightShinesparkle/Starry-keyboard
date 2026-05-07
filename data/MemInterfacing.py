import board
import busio
import data.Mem24lc16 as Mem24lc16
import data.MemMisc as Misc
import keysys.KeyTypes as KeyTypes

i2c : busio.I2C = busio.I2C(board.GP11,board.GP10)

EEProm : Mem24lc16.Mem24LC16 = Mem24lc16.Mem24LC16(i2c)

# Print EEPROM length
def PrintLen():
	print(f"Initialized with EEPROM length of {len(EEProm)}")

# Clear EEPROM data
def ClearData():
	for x in range(EEProm.Length):
		EEProm[x] = 0

# Load default data
def LoadDefaults():
	ClearData()
	Ptr : int = 0
	for x in Misc.MAGICNO:
		EEProm[Ptr] = x
		Ptr += 1

	for x in Misc.DEFAULTDATA:
		EEProm[Ptr] = x
		Ptr += 1
	EEProm[Ptr] = Misc.FILEEND

# Reads block data from EEPROM
# Data may be found in the following format:
# [Magic number] -> blocks
# Blocks may be found in the following format:
# 0x01 [ENUM] 			| 2 bytes, second byte is directly loadable
# 0x02 [Size] [N ENUM] 	| Size +2 bytes
# 0x03 [Size] [Text]   	| Size +2 bytes
# 0x04 					| End
def LoadBlocks(Modifiable : list[list[KeyTypes.BaseKey]]):
	Ptr : int = len(Misc.MAGICNO)
	XPos : int = 0
	YPos : int = 0

	# Max board X and Y button coords
	MaxY : int = len(Modifiable)
	MaxX : int = len(Modifiable[0])

	while True:
		if (Ptr >= EEProm.Length) or (YPos >= 5):
			break

		BlockType : int = EEProm[Ptr]

		if BlockType == 0x01:
			Data : int = EEProm[Ptr+1]
			Ptr += 2
			# Create normal key and store in array
			Modifiable[YPos][XPos] = KeyTypes.NormalKey(Data)

		elif BlockType == 0x02:
			Size : int = EEProm[Ptr+1]
			Ptr += 2
			Data : list = []
			# Create multiple keypress key and store in array
			NewKey : KeyTypes.MultipressKey = KeyTypes.MultipressKey()
			
			for x in range(Size):
				Data.append(EEProm[Ptr])
				Ptr += 1

			NewKey.Data = Data
			Modifiable[YPos][XPos] = NewKey

		elif BlockType == 0x03:
			Size : int = EEProm[Ptr+1]
			Ptr += 2
			Data = ""
			# Create text key and store in array
			NewKey : KeyTypes.TextWriterKey = KeyTypes.TextWriterKey()

			for x in range(Size):
				Data += chr(EEProm[Ptr])
				Ptr += 1

			NewKey.Data = Data
			Modifiable[YPos][XPos] = NewKey


		elif BlockType == 0x04:
			break

		else:
			Ptr += 1
			continue

		XPos += 1
		if XPos >= MaxX:
			XPos = 0
			YPos += 1

			if YPos >= MaxY:
				# Data overflow
				break



# Function to preload the needed data for the calc
def Preload(Modifiable : list[list[KeyTypes.BaseKey]]):
	# Checks if it has viable preloaded data
	Loadable : bool = True

	print("Loading data from EEPROM...")

	for x in range(len(Misc.MAGICNO)):
		Val : int = Misc.MAGICNO[x]
		Stored : int = EEProm[x]
		if (Val != Stored):
			Loadable = False
			break
	
	print("Found viable data!" if Loadable else "Loading default data...")
	if not Loadable:
		LoadDefaults()
		print("Loaded default data")

	try:
		LoadBlocks(Modifiable)
	except Exception as E:
		print("Error loading data")
		print(str(E))
