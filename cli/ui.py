def clearTerm():
	print(chr(27) + "[2J" + chr(27) + "[0;0H", end = "")
def doNothing(selection):
	pass

''' 
Are you sure you would like to continue? [y/N]
The message parameter determines the message

Returns True if yes, False if no
'''
def areYouSure(message = "Are you sure you would like to continue [y/N]? "):
	response = input(message)
	response = response.strip()
	if(response.startswith("y") or response.startswith("Y")):
		return True
	return False
''' 
Menu header goes here:
	0 - Option: OptionDesc
	1 - Option: OptionDesc
	2 - Option: OptionDesc
	3 - Option: OptionDesc
Prompt goes here? The MenuEntry selected is returned, or None if the value is invalid

Options are specified by an array of MenuEntry objects:
Description can be None to just print the name
If the name and description are None, then the description is printed without actually being an option
If both the Description and Name are None a newline will be printed
If the event of the menu entry it will be called if that entry is selected
If the customHead is set then it will be used instead of the objHead variable of the menu() function
If the areYouSure variable is True then an "Are you sure" prompt will be shown

repeatOnError:    can be set to True to repeat if the user enters an invalid response     (default True)
repeatNormally:   can be set to True to repeat even if the user enters a valid response   (default False)
clear:            can be set to True to also clear the terminal                           (default False)
objHead:          can be set to whatever and it will add a prefix to the option           (default "  ")
onSelect:         can be set and will be called with a the selected MenuEntry             (default doNothing)
'''
class MenuEntry:
	def __init__(self, name, desc = None, event = None, customHead = None, areYouSure = False):
		self.name = name
		self.desc = desc
		self.event = event
		self.areYouSure = areYouSure
		self.customHead = customHead
#I spent WAY too much time on this
def menu(header, entries, prompt, repeatNormally = False, repeatOnError = True, clear = False, objHead = "  ", onSelect = doNothing):
	while(True):
		#Print the menu
		if(clear):
			clearTerm()
		print(header)
		m = type(MenuEntry("menu" , "entry"))
		visibleEntries = []
		entryId = 0
		for e in entries:
			if(type(e) != m):
				raise TypeError("Invalid type! Must be a MenuEntry object!")
			head = objHead
			#Custom head
			if(e.customHead != None):
				head = e.customHead
			#Custom sub-headings/newlines
			if(e.name == None or (not e.name)):
				if(e.desc == None or (not e.desc)): 
					print()
				else: 
					print(head + e.desc)
				continue
			#Typical application 
			head = head + str(entryId) + " - "
			if(e.desc == None or (not e.desc)): 
				print(head + e.name)
			else: 
				print(head + e.name + ": " + e.desc)
			visibleEntries.append(e)
			entryId = entryId + 1
		#User input handling
		response = input(prompt)
		selection = -1
		error = True
		try:
			selection = int(response)
			if(selection < 0 or selection >= len(visibleEntries)):
				raise IndexError
			error = False
		except ValueError:
			print("Selection must be a number")
		except IndexError:
			print("Invalid selection (out of range)")
		#Error handling
		if(error or selection < 0):
			if(not repeatOnError):
				return None
			else:
				continue
		#Is the user sure of there decision
		if(visibleEntries[selection].areYouSure):
			if(not areYouSure()):
				return None
		#Call the event handlers
		if(visibleEntries[selection].event != None):
			visibleEntries[selection].event()
		onSelect(visibleEntries[selection])
		#Repeat or not repeat
		if(repeatNormally):
			continue
		else:
			return visibleEntries[selection]


  
