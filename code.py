# General misc
import time
import digitalio
import board

# USB HID
import usb_hid

# Adafruit HID keyboard misc
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# Modules
import keys

# Keyboard and layout init
Kbd = Keyboard(usb_hid.devices)
Layout = KeyboardLayoutUS(Kbd)

keys.SetupKeys()

while True:
	keys.ScanRoutine()
	time.sleep(0.001)