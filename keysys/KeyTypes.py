from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Obj with an executable within
# Will hold the data to use
# Has a function for pressing and unpressing

class BaseKey:
	def Press(self, Kbd : Keyboard, Layout : KeyboardLayoutUS = None) -> None:
		pass

	def Unpress(self, Kbd : Keyboard, Layout : KeyboardLayoutUS = None) -> None:
		pass

	@property 
	def Weight(self) -> int:
		pass

	@property
	def JSONParsed(self) -> str:
		pass

# Normal key press
class NormalKey(BaseKey):
	def __new__(cls, Code : int = None):
		if Code is not None:
			return NormalKey.Create(Code)
		else:
			return super().__new__(cls)

	def Create(Code : int):
		Key : NormalKey = NormalKey()
		Key.Data = Code
		return Key

	Data : int = 0
	def Press(self, Kbd : Keyboard, Layout : KeyboardLayoutUS) -> None:
		Kbd.press(self.Data)

	def Unpress(self, Kbd : Keyboard, Layout : KeyboardLayoutUS) -> None:
		Kbd.release(self.Data)

	@property
	def Weight(self) -> int:
		return 1
	
	@property
	def JSONParsed(self) -> str:
		return f"{{\"Type\":1,\"Data\":{self.Data}}}"

# Presses multiple keys at the same time
class MultipressKey(BaseKey):
	Data : list = [0]
	def Press(self, Kbd : Keyboard, Layout : KeyboardLayoutUS = None) -> None:
		for code in self.Data:
			Kbd.press(code)

	def Unpress(self, Kbd : Keyboard, Layout : KeyboardLayoutUS = None) -> None:
		for code in self.Data:
			Kbd.release(code)

	@property
	def Weight(self) -> int:
		return len(self.Data)
	
	@property
	def JSONParsed(self) -> str:
		Returnable : str = f"{{\"Type\":2,\"Data\":["
		for Chr in self.Data:
			Returnable += f"{Chr},"
		Returnable = Returnable[:-1] + f"]}}"
		return Returnable

# Writes a whole text
class TextWriterKey(BaseKey):
	Data : str = ""
	def Press(self, Kbd : Keyboard, Layout : KeyboardLayoutUS = None) -> None:
		Kbd.release_all()
		Layout.write(self.Data,0.05)

	def Unpress(self, Kbd : Keyboard, Layout : KeyboardLayoutUS = None) -> None:
		pass

	@property
	def Weight(self) -> int:
		return 8
	
	@property
	def JSONParsed(self) -> str:
		return f"{{\"Type\":3,\"Data\":{self.Data}}}"