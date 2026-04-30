import board
import digitalio
import setup
import time

# Temporal stuffs....
# Adafruit HID keyboard misc
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import usb_hid
from keysys.KeyTypes import NormalKey
from keysys.KeyTypes import BaseKey

Kbd : Keyboard = Keyboard(usb_hid.devices)
Layout : KeyboardLayoutUS = KeyboardLayoutUS(Kbd)

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
	board.GP5, board.GP6, board.GP7, board.GP8, board.GP9
]

# Keyboard input pints
KeyboardInputs = [
	board.GP0, board.GP1, board.GP2, board.GP3, board.GP4
]

# Keyboard LED pins
KeyboardLEDCapsLock = None 
KeyboardLEDNumLock = None 
KeyboardLEDScrollLock = None

# Loaded pins
KeyboardOutputsLoaded : list[digitalio.DigitalInOut] = []
KeyboardInputsLoaded : list[digitalio.DigitalInOut] = []

# Key lists
KeysJustPressed : list[list[int]] = []	# Keys that just got pressed
KeysPressing : list[list[int]] = []		# Keys that are being pressed

# Key press quantity
KeyPressQuantity = 0

# Temporal key array thingy
TempKeys : list[list[BaseKey]] = [
	[NormalKey(Keycode.M),NormalKey(Keycode.O),NormalKey(Keycode.N),NormalKey(Keycode.L),NormalKey(Keycode.I)],
	[NormalKey(Keycode.G),NormalKey(Keycode.H),NormalKey(Keycode.T),NormalKey(Keycode.W),NormalKey(Keycode.A)],
	[NormalKey(Keycode.S),NormalKey(Keycode.E),NormalKey(Keycode.R),NormalKey(Keycode.SEMICOLON),NormalKey(Keycode.THREE)],
	[NormalKey(Keycode.SPACE),NormalKey(Keycode.ENTER),NormalKey(Keycode.LEFT_SHIFT),NormalKey(Keycode.CAPS_LOCK),NormalKey(Keycode.BACKSPACE)],
	[NormalKey(Keycode.O),NormalKey(Keycode.U),NormalKey(Keycode.PERIOD),NormalKey(Keycode.EQUALS),NormalKey(Keycode.MINUS)]
]

def JSONStringify() -> str:
	Returnable : str = "{\"Keys\":["
	for Line in TempKeys:
		for Key in Line:
			Returnable += Key.JSONParsed+","
	Returnable = Returnable[:-1] + "]}"
	return Returnable

def SetupKeys() -> None:
	"""Prepares keyboard IO pins and stores them into the loaded arrays"""

	global KeysJustPressed
	global KeysPressing

	global KeyboardLEDCapsLock
	global KeyboardLEDNumLock
	global KeyboardLEDScrollLock

	if KeyboardLEDCapsLock is None:
		KeyboardLEDCapsLock = setup.SetupOutput(board.GP12)
	
	if KeyboardLEDNumLock is None:
		KeyboardLEDNumLock = setup.SetupOutput(board.GP13)

	if KeyboardLEDScrollLock is None:
		KeyboardLEDScrollLock = setup.SetupOutput(board.GP14)

	KeysJustPressed.clear()
	KeysPressing.clear()

	for Inpin in KeyboardInputs:
		Pin : digitalio.DigitalInOut = setup.SetupOutput(Inpin)
		Pin.value = 1
		KeyboardInputsLoaded.append(Pin)
		KeysJustPressed.append([])
		KeysPressing.append([])
	
	for Outpin in KeyboardOutputs:
		Pin : digitalio.DigitalInOut = setup.SetupInput(Outpin, digitalio.Pull.UP)
		KeyboardOutputsLoaded.append(Pin)

def ScanRoutine() -> None:
	"""Routine for scanning through all keys"""
	global KeysJustPressed
	global KeysPressing
	global KeyPressQuantity

	KeyboardLEDCapsLock.value = Kbd.led_on(Kbd.LED_CAPS_LOCK)
	KeyboardLEDNumLock.value = Kbd.led_on(Kbd.LED_NUM_LOCK)
	KeyboardLEDScrollLock.value = Kbd.led_on(Kbd.LED_SCROLL_LOCK)

	# Current matrix pawsitions
	CurrXPos = 0
	CurrYPos = 0

	for y in KeyboardInputsLoaded:
		CurrXPos = 0
		y.value = 0
		time.sleep(0.000015)

		KeysJustPressedEntries : list[int] = KeysJustPressed[CurrYPos]
		KeysPressingEntries : list[int] = KeysPressing[CurrYPos]

		for x in KeyboardOutputsLoaded:
			# Adafruit states max 8 keys pressing at once
			if not x.value and (KeyPressQuantity <= 8):
				# Check if key is in KeysJustPressedEntries list
				if CurrXPos in KeysJustPressedEntries:
					KeysPressingEntries.append(CurrXPos)
					KeysJustPressedEntries.remove(CurrXPos)
					#print("Still pressing "+str(CurrXPos)+", "+str(CurrYPos))

				# Check if key is not in KeysPressingEntries
				elif not (CurrXPos in KeysPressingEntries):
					KeysJustPressedEntries.append(CurrXPos)
					#print("Just pressed "+str(CurrXPos)+", "+str(CurrYPos))
					Pressable : BaseKey = TempKeys[CurrYPos][CurrXPos]
					Pressable.Press(Kbd,Layout)
					KeyPressQuantity += Pressable.Weight
			# Check if key is in KeysPressingEntries
			elif CurrXPos in KeysPressingEntries:
				# Remove from KeysPressingEntries
				KeysPressingEntries.remove(CurrXPos)
				Pressable : BaseKey = TempKeys[CurrYPos][CurrXPos]
				Pressable.Unpress(Kbd,Layout)
				KeyPressQuantity -= Pressable.Weight
				#print("Released "+str(CurrXPos)+", "+str(CurrYPos))
			
			elif CurrXPos in KeysJustPressedEntries:
				# Remove from KeysJustPressedEntries
				KeysJustPressedEntries.remove(CurrXPos)
				Pressable : BaseKey = TempKeys[CurrYPos][CurrXPos]
				Pressable.Unpress(Kbd,Layout)
				KeyPressQuantity -= Pressable.Weight
				#print("Released "+str(CurrXPos)+", "+str(CurrYPos))

			CurrXPos += 1

		y.value = 1
		CurrYPos += 1