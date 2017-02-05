import string
import enum
import time
import random
import threading
import _thread
from pynput import keyboard
from os import system

print ("Hej jag heter Simone!")
system('say -v Alva "Hej jag heter Simone!"')

# globals
numberOfPeopleInRoom = 0
currentRoomEvents = []


# read the file containing states and what to say
try:
	inFile = open("simonescript.txt", encoding='utf-8')
except OSError:
	#File not found
	print("File not found")
content = inFile.readlines()
inFile.close()


# room events
from enum import Enum, auto
class RoomEvent(Enum):
	ALL_IN_LINE = "ALL_IN_LINE"
	PERSON_ENTERS_ROOM = "PERSON_ENTERS_ROOM"
	PERSON_LEAVES_ROOM = "PERSON_LEAVES_ROOM"
	PERSON_GETS_IN_LINE = "PERSON_GETS_IN_LINE"
	ALL_IN_LINE_TIMOUT = "ALL_IN_LINE_TIMOUT"
	ROOM_IS_EMPTY = "ROOM_IS_EMPTY"
	MANY_PEOPLE_IN_ROOM = "MANY_PEOPLE_IN_ROOM"
	PERSON_LEAVES_LINE = "PERSON_LEAVES_LINE"


# functions Start

def addState(key):
	global currentRoomEvents
	
	if key == keyboard.Key.alt:
		addRoomEvent(currentRoomEvents, RoomEvent.ALL_IN_LINE)
	elif key == keyboard.Key.shift:
		addRoomEvent(currentRoomEvents, RoomEvent.PERSON_ENTERS_ROOM)
	elif key == keyboard.Key.ctrl:
		addRoomEvent(currentRoomEvents, RoomEvent.PERSON_GETS_IN_LINE)
	elif key == keyboard.Key.cmd:
		addRoomEvent(currentRoomEvents, RoomEvent.PERSON_LEAVES_LINE)


def removeState(key):
	global currentRoomEvents

	if key == keyboard.Key.alt:
		removeRoomEvent(currentRoomEvents, RoomEvent.ALL_IN_LINE)
	elif key == keyboard.Key.shift:
		removeRoomEvent(currentRoomEvents, RoomEvent.PERSON_ENTERS_ROOM)
	elif key == keyboard.Key.ctrl:
		removeRoomEvent(currentRoomEvents, RoomEvent.PERSON_GETS_IN_LINE)
	elif key == keyboard.Key.cmd:
		removeRoomEvent(currentRoomEvents, RoomEvent.PERSON_LEAVES_LINE)


def addRoomEvent(eventList, event):
	eventList.append(event)
	print("Added event %s" % event.name)
#	if(len(eventList)>0):
#		print("Added event %s" % eventList[len(eventList)-1])

def removeRoomEvent(eventList, event):
	if event in eventList:
		eventList.remove(event)
		print("Removed event %s" % event.name)

def on_press(key):
	addState(key)
#	try:
#		print('alphanumeric key {0} pressed'.format(key.char))
#	except AttributeError:
#		print('special keuy {0} pressed'.format(key))
		

def on_release(key):
	if key == keyboard.Key.esc:
		#stop listener
		return False
	removeState(key)

def keyListener( tname ):
	with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
		listener.join()

def getSpeechCandidates():
	if len(currentRoomEvents) == 0: 
		return

#	print(currentRoomEvents)
	room_events = []
	for event in currentRoomEvents:
		room_events.append(event.name)

	speechCandidates = []
	
	# content - is the text file containing states and what to say
	# currentRoomState - the states the room is in at the moment
	
	state_match = False
	
	# go through the script and find next state (a line that starts with +)
	for line in content:
		plus_line = line.find('+')
		if plus_line > -1:
			state_match = False
			states = line.split(':')

			# check if the STATES match current room state.
			for state in states:
				state = state.translate({ord(c): None for c in '+-'}) # strip any + och -
				state = state.strip() # strip any white space
				if state in room_events:
					state_match = True
		
		# if we have a state match, add the following lines in script until next state
		else:
			if state_match:
				speechCandidates.append(line)
	
	return(speechCandidates)

# Functions End

def talk():
	global content
	global currentRoomEvents
	if len(currentRoomEvents) == 0:
		return
	# a list of possible scentences to say 
	speechCandidates = getSpeechCandidates()
	# print(speechCandidates)
	if(len(speechCandidates)>0):
		sentence_to_say = random.choice(speechCandidates)
		sentence_to_say = sentence_to_say.strip()
		print(sentence_to_say)
		system_say_command = format('say -v Alva {}'.format(sentence_to_say))
		system(system_say_command)


def main():
	lastFrameTime = 0
	print("main")

	while True:
		currentTime = time.time()
		deltaTime = currentTime - lastFrameTime

		if(deltaTime > 3):
			lastFrameTime = currentTime
			talk()

_thread.start_new_thread(keyListener,("keylistener", ))

main()

