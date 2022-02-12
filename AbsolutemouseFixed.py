# Code based on:https://forums.frontier.co.uk/threads/so-you-want-a-relative-mouse-toggle-here-it-is-diy-guide.379166/post-8305997
#
# There are hotkeys at the bottom that will need to be set to yours

# Modifications made by Cmdr Jackblack2001
 
from System import Int16

#imported time library to use on headlook hotkey section down below (makes possible the use of sleep method)
import time

# set globals
if starting:
	isEnabled = True
	mouseX	= mouseY = mouseXcurved = mouseYcurved = 0
	MAX =  Int16.MaxValue * 0.5 + 0.5  #  16384
	MIN = -Int16.MaxValue *0.5 - 0.5   # -16384
	
	# Timer, for auto-centering
	system.setThreadTiming(TimingTypes.HighresSystemTimer)	
	system.threadExecutionInterval = 1 # loop delay - controls how often the script updates -- 5 is fine, lower for more updates (1 = 1000 times per second, 2 = 500, etc.)
	device = vJoy[0] #Your divice, you have to change this according to your device index (the number of the device on the vJoy Config -1)
 
 
	#-----------------------------------------------------------------------------------------------
	ABSOLUTE_SENSITIVITY = 28    # absolute mouse mode overall sensitivity.  Default: 28	
	ABSOLUTE_CURVE = 1.0  	     # NON-ALTERNATE: The exponent for mouse acceleration.  Default: 1.0 = no acceleration.
	#-----------------------------------------------------------------------------------------------
	# Essentially, this acts as a "soft" deadzone while also helping you make precise movements for aiming. 
	CENTERING_RADIUS = 1000   # Centering radius.  The actual radius will be less than this if ABSOLUTE_CURVE is greater than 1.0.  Default: 100	
	CENTERING_SPEED = 1       # Linear centering speed.  MUST be less than ABSOLUTE_DEADZONE.  0 to this feature completely disable.  Default: 1
	#-----------------------------------------------------------------------------------------------	
	# Essentially, this is mouse acceleration for the absolute mouse mode.
	USE_ALTERNATE_ABSOLUTE_CURVE = False         # The most important difference is that the non-alternate version can be configured to have no mouse acceleration at all.
	ALTERNATE_ABSOLUTE_CURVE_FACTOR1 = 0.5       # ALTERNATE: Essentially mouse acceleration.  Higher = faster movement. Default: 0.5
	ALTERNATE_ABSOLUTE_CURVE_FACTOR2 = 0.015625  # ALTERNATE: Essentially mouse acceleration.  Higher = faster movement. Default: 0.015625
	#-----------------------------------------------------------------------------------------------	
	ABSOLUTE_DEADZONE = 2        # Recommended to not go below 2
	#-----------------------------------------------------------------------------------------------	
	# Some idiot checks
	# Idiotic, but rather functional... ;3
	if (ABSOLUTE_DEADZONE < 2): ABSOLUTE_DEADZONE = 2 
	if (CENTERING_SPEED >= ABSOLUTE_DEADZONE) or (CENTERING_SPEED < 0): CENTERING_SPEED = ABSOLUTE_DEADZONE - 1 
	ABSOLUTE_CURVE_RATIO = (MAX ** ABSOLUTE_CURVE ) / MAX   # NON-ALTERNATE: not intended to be modified
	flip = True
 
def getClamped(val):
	if (val > MAX): val = MAX
	elif (val < MIN): val = MIN
	return val
 
def getCentering(val):
	if (val < CENTERING_RADIUS) and (val > 0): val -= CENTERING_SPEED
	elif (val > -(CENTERING_RADIUS)) and (val < 0): val += CENTERING_SPEED
	return val
 
def getAbsoluteCurve(val):
	val2 = 0
	if (val > 0): 
		val2 = math.floor((val ** ABSOLUTE_CURVE) / ABSOLUTE_CURVE_RATIO) 
	elif (val < 0):
		val = -(val)
		val2 = -(math.floor((val ** ABSOLUTE_CURVE) / ABSOLUTE_CURVE_RATIO))
	return val2
 
def getAlternativeAbsoluteCurve(val):
	val2 = 0
	if (val > 0): val2 = math.floor((math.sqrt(val ** 3) * ALTERNATE_ABSOLUTE_CURVE_FACTOR1) * ALTERNATE_ABSOLUTE_CURVE_FACTOR2)
	elif (val < 0): val2 = math.floor(-abs(math.sqrt(abs(mouseX ** 3)) * ALTERNATE_ABSOLUTE_CURVE_FACTOR1 ) * ALTERNATE_ABSOLUTE_CURVE_FACTOR2)
	return val2
 
if (isEnabled):
	# get change in mouse position, multiply by sensitivity setting, and then clamp the values to those supported by the joystick device
	mouseX  += mouse.deltaX * ABSOLUTE_SENSITIVITY   # absolute mouse
	mouseX  = getClamped(mouseX)
	mouseY  += mouse.deltaY * ABSOLUTE_SENSITIVITY  
	mouseY  = getClamped(mouseY)	
 
	############################ Absolute Mouse	
 
	mouseX = getCentering(mouseX)
	mouseY = getCentering(mouseY)
 
	if (USE_ALTERNATE_ABSOLUTE_CURVE): 
		mouseXcurved = getAlternativeAbsoluteCurve(mouseX)
		mouseYcurved = getAlternativeAbsoluteCurve(mouseY)
	else: 	
		mouseXcurved = getAbsoluteCurve(mouseX)
		mouseYcurved = getAbsoluteCurve(mouseY)
 
	device.x = filters.deadband(mouseXcurved, ABSOLUTE_DEADZONE)
	device.y = filters.deadband(mouseYcurved, ABSOLUTE_DEADZONE)
 
 
	################################ Watch (debug)
	diagnostics.watch(device.x)
	diagnostics.watch(device.y)
	
	
 
# Fixes drifting when using headlook key (my headlook key is: The middle mouse Button)
if mouse.middleButton: #if you're using an keyboard key, use --> keyboard.getPressed(Key."Your key here (Ex: NumberPad1)")

	#if you are using an KB Key delete the "time.sleep" line (this comments are useless to :3)
	#This timer is for the script "accept" my key, cuz for some reason its triggered every ms when pressed
	#The optimal is 0.4
	time.sleep(0.4)
	
	if isEnabled:
		isEnabled = False
				
	else:
		isEnabled = True
		#If you want to center your ship after using headlook, uncomment this line
		#mouseX = mouseXcurved = mouseY = mouseYcurved = 0
		
		mouseX  -= mouse.deltaX
		mouseY  -= mouse.deltaY
		
#diagnostics.watch(isEnabled)
		
#Same as the headlook HotKey, for -->
#Steam Overlay
if keyboard.getPressed(Key.F9):
			
	if isEnabled:
		isEnabled = False
	else:
		isEnabled = True

#Discord Overlay
if keyboard.getPressed(Key.F10):
			
	if isEnabled:
		isEnabled = False
	else:
		isEnabled = True

#Galaxy Map
if keyboard.getPressed(Key.NumberPadEnter):
			
	if isEnabled:
		isEnabled = False
	else:
		isEnabled = True

#System Map
if keyboard.getPressed(Key.NumberPadPlus):
			
	if isEnabled:
		isEnabled = False
	else:
		isEnabled = True
	
# When leaving the station, press this key to center. Does the same as above, but doesnt mess up with the Flight Assist key
if keyboard.getPressed(Key.V):
	if not isEnabled:
		isEnabled = True
	mouseX = mouseXcurved = mouseY = mouseYcurved = 0
        
# Centers mouse when switching to FA-On from FA-Off (my FA-on/off key is: CapsLock)
if keyboard.getPressed(Key.CapsLock):
	mouseX = mouseXcurved = mouseY = mouseYcurved = 0
	# This line is an Auto-AlternateFlight-Changer, so when you press the FA key, automaticly it changes to the right one
	# **Disclaimer** You will have to manualy switch to absolute mode upon reopening the game, using your in game key
	keyboard.setPressed(Key.Tab)