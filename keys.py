import board
import digitalio
import setup
import time

'''
║ *- Inpin & Outpin are keyboard based														   ║
║	   KBD							 Pico													   ║
║	 ╔═════╗						╔════╗													   ║
║	 ╠═════╣			Inpin		║	 ║													   ║
║	 ║	   ║ <┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅ ║	 ║													   ║
║	 ║	   ║ ┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅> ║	 ║													   ║
║	 ╚═════╝			Outpin		╚════╝													   ║
║																							   ║
'''

# Keyboard output pins
KeyboardOutputs = [
	board.GP5, board.GP6, board.GP7, board.GP8
]

# Keyboard input pints
KeyboardInputs = [
	board.GP0, board.GP1, board.GP2, board.GP3, board.GP4
]

# Loaded pins
KeyboardOutputsLoaded = []
KeyboardInputsLoaded = []

# Key lists
KeysJustPressed = []	# Keys that just got pressed
KeysPressing = []		# Keys that are being pressed
KeyTimeRegistries = []	# How long they have been pressed

# Time registry pressed again
KeySpamDelay = 0.1

def SetupKeys() -> None:
	"""Prepares keyboard IO pins and stores them into the loaded arrays"""

	global KeysJustPressed
	global KeysPressing
	global KeyTimeRegistries

	KeysJustPressed.clear()
	KeysPressing.clear()
	KeyTimeRegistries.clear()

	for Inpin in KeyboardInputs:
		Pin = setup.SetupOutput(Inpin)
		Pin.value = 1
		KeyboardInputsLoaded.append(Pin)
		KeysJustPressed.append([])
		KeysPressing.append([])
		KeyTimeRegistries.append([])
	
	for Outpin in KeyboardOutputs:
		Pin = setup.SetupInput(Outpin, digitalio.Pull.UP)
		KeyboardOutputsLoaded.append(Pin)
		for Entry in KeyTimeRegistries:
			Entry.append(0)

def ScanRoutine() -> None:
	"""Routine for scanning through all keys"""
	global KeysJustPressed
	global KeysPressing
	global KeyTimeRegistries

	# Current matrix pawsitions
	CurrXPos = 0
	CurrYPos = 0

	for y in KeyboardInputsLoaded:
		CurrXPos = 0
		y.value = 0
		time.sleep(0.000015)

		KeysJustPressedEntries : list = KeysJustPressed[CurrYPos]
		KeysPressingEntries : list = KeysPressing[CurrYPos]

		for x in KeyboardOutputsLoaded:
			if not x.value:
				# Check if key is in KeysJustPressedEntries list
				if CurrXPos in KeysJustPressedEntries:
					KeysPressingEntries.append(CurrXPos)
					KeysJustPressedEntries.remove(CurrXPos)
					print("Still pressing "+str(CurrXPos)+", "+str(CurrYPos))

				# Check if key is not in KeysPressingEntries
				elif not (CurrXPos in KeysPressingEntries):
					KeysJustPressedEntries.append(CurrXPos)
					print("Just pressed "+str(CurrXPos)+", "+str(CurrYPos))

				# Check if key is in KeysPressingEntries
				else:
					# Continously effectuate action
					pass
			# Check if key is in KeysPressingEntries
			elif CurrXPos in KeysPressingEntries:
				# Remove from KeysPressingEntries
				KeysPressingEntries.remove(CurrXPos)
				print("Released "+str(CurrXPos)+", "+str(CurrYPos))
			elif CurrXPos in KeysJustPressedEntries:
				# Remove from KeysJustPressedEntries
				KeysJustPressedEntries.remove(CurrXPos)
				print("Released "+str(CurrXPos)+", "+str(CurrYPos))

			CurrXPos += 1

		y.value = 1
		CurrYPos += 1