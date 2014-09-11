#
# sectalks 0x03 challenge server
#
# This file defines the following classes:
#  - Object: Items the player interacts with in the game (desk, bin, documents)
#  - Room: Where the player is currently "located". Determines what objects are available to interact with
#

class Object:
	look_commands = ['look', 'gaze', 'explore', 'investigate', 'probe', 'poke', 'open', 'walk', 'open', 'hit', 'write', 'sit', 'go', 'pull']
	get_commands = ['get', 'take', 'pickup', 'lift', 'add', 'retrieve']
	use_commands = ['use', 'deploy', 'wield', 'hold', 'utilise', 'utilize', 'unlock']
	valid_commands = look_commands + get_commands + use_commands

	def __init__(self, description):
		self.parent = None

		# This function is called as f(self, name, user) when the object is
		# added to inventory
		self.ongetcallback = None

		self.description = ""
		for line in description.split("\n"):
			self.description += line.strip() + "\r\n"

		self.objects = {}
		self.actions = {}

		# Dictionary of functions that are called as f(self, name, command, user) - defined per-object for custom interactions
		self.cmd_hooks = {}
		self.hardtoget = False

	def interact(self, name, command, user):
		# Unknown commands get an error
		if command not in (Object.valid_commands + self.cmd_hooks.keys()):
			user.naughtycount += 1
			user.write("What?")
			user.write("")
			user.prompt()
			return

		# Execute custom command hook
		if command in self.cmd_hooks.keys():
			f = self.cmd_hooks[command]
			return f(self, name, command, user)

		if command in self.look_commands:
			user.write(self.description)
			# This is terrible but I'm so tired and this needs to be finished :'(
			if name in ['desk', 'table'] and user.foundkey:
				user.write("An old-fashioned key is sitting next to the folder.")
				user.write("")
		elif command in self.get_commands:
			if self.hardtoget and not user.username == 'admin':
				user.write('You can\'t seem to pick up the %s. Perhaps an admin can do this for you.' % (name)) 
			else:
				user.write('You pick up the %s' % (name)) 
				if not user.addInventory(name, self):
					user.write("")
					user.write('Unfortuntely, the %s slips through your fingers and rolls away under a nearby couch! :\'(' % (name)) 
			
			user.write("")
		elif command in self.use_commands:
			if name in user.inventory.keys():
				user.lookingAt.use(self, user)
			else:
				user.write("You don't have a %s!" % name)
				user.write("")
		else:
			user.write("You want to do what?")
			user.write("")

	def addObject(self, names, o):
		for n in names:
			self.objects[n] = o

		o.parent = self

	def addAction(self, obj, f):
		"""
		Function f is called with argument user when obj is used on self.
		"""
		self.actions[obj] = f

	def use(self, obj, user):
		"""
		Object obj is used on self
		"""
		if obj in self.actions.keys():
			f = self.actions[obj]
			f(user)
		else:
			user.write("Nothing happens!")
			user.write("")

class Room:
	def __init__(self, description):
		"""
		objects is a list of tuples, arguments to the Object constructor

		description - string
		objects - list of tuples (name, object_constructor)
		"""

		self.parent = None

		self.description = ""
		for line in description.split("\n"):
			self.description += line.strip() + "\r\n"

		self.objects = {}

	def entry(self):
		"""
		Return text to be printed when we enter this room
		"""
		return self.description

	def addObject(self, names, o):
		for n in names:
			self.objects[n] = o

		o.parent = self

	def use(self, obj, user):
		user.write("Nothing happens!")

