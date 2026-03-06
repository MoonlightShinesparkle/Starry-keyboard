# General misc
import time

# Modules
import keys
import saving

# Delegate key misc to keys module
keys.SetupKeys()

saving.PrintLen()
saving.TestWrite()

# Constantly scan for key presses
while True:
	keys.ScanRoutine()
	time.sleep(0.00075)