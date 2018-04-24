from cli.ui import clearTerm, menu, MenuEntry
from time import sleep

def helloWorld():
	print("Hello world!")
	input("Press enter to continue!")
def primes():
	s = int(input("Number to start at? "))
	e = int(input("Number to stop at? "))
	if(e > s):
		input("Press enter to continue!")
		return
	nums = ""
	for n in range(s, e):
		if(n % 2 == 0 or n < 1):
			continue
		prime = True
		for i in range(3, n - 1, 2):
			if(n % i == 0):
				prime = False
				break
		if(not prime):
			continue
		nums = nums + str(n) + ", "
	nums = nums[0:-2]
	print(nums)
	input("Press enter to continue!")
def fib():
	am = int(input("Amount? "))
	a = 0
	b = 0
	r = 1
	nums = "0, "
	for i in range(0, am):
		b = a
		a = r
		nums = nums + str(r) + ", "
		r = a + b
	nums = nums[0:-2]
	print(nums)
	input("Press enter to continue!")

todoItems = []
def todo():
	while True:
		clearTerm()
		entries = []
		for i in todoItems:
			item = MenuEntry("Item", i)
			entries.append(item)
			item.associatedItem = i
		create = MenuEntry("Create", "Creates a new item")
		entries.append(create)
		exit = MenuEntry("Exit", "Leaves the menu")
		entries.append(exit)

		selection = menu("Todo list: ", entries, "Select an item to modify: ", repeatNormally = False, repeatOnError = True, clear = False)
		if(selection == exit):
			return
		elif(selection == create):
			name = input("What do you need to do? ")
			todoItems.append(name)
			print("Successfully created todo item: " + name)
			continue
		else:
			delete = MenuEntry("Delete", None, areYouSure = True)
			edit = MenuEntry("Edit", None)
			cancel = MenuEntry("Cancel", None)
			subSelection = menu("Available actions", [delete, edit, cancel], "Action: ", repeatNormally = False, repeatOnError = True, clear = False)
			if(subSelection == delete):
				todoItems.remove(selection.associatedItem)
				continue
			if(subSelection == edit):
				item = selection.associatedItem
				todoItems.remove(item)
				item = input("Enter the new item's name: ")
				todoItems.append(item)
				continue
	
entries = [
	MenuEntry(None, "Random: ", customHead = " "),
	MenuEntry("Hello world!", "Prints \"Hello world!\" to console", helloWorld),
	MenuEntry("Todo list", "Example todo list made using the menu system", todo),
	MenuEntry(None, "Mathematics: ", customHead = " "),
	MenuEntry("Primes", "Gets the prime numbers in a specified range", primes),
	MenuEntry("Fibonicci", "Runs the fibinicci sequence for x iterations", fib),
	MenuEntry("Exit", "Stops the program", exit)
]
res = menu("Select an action from the list of actions!", entries, "Action? ", repeatNormally = True, clear = True)
