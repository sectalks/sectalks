#!/usr/bin/python
#
# sectalks 0x03 challenge server
#
# This file  contains the main server loop - receive connections from clients,
# track sessions in User objects and pass commands to the appropriate User
# object.
#
# Class User tracks the state of a single client session per instance; eg. the
# Room object they currecntly inhabit, or any items in their inventory.
#

import socket
import select
import string
import random
import sqlite3
import sys

from Crypto.Cipher import ARC4

from classes import Room, Object
from game import room_start, r2, r3

TILT_NAUGHTY = 7
MAX_NAUGHTY = 10

class CryptoError(Exception):
	"""Crypto decode error"""
	pass

class ParseError(Exception):
	"""User input is inappropriate"""
	pass

class User:
	def __init__(self, s, cipher, debug=False):
		# Constructor
		self.ip = s.getpeername()
		self.cipher = cipher
		self.sock = s
		self.debug = debug

		self.inventory = {}
		self.lookingAt = None
		self.post = []
		self.naughtycount = 0
		self.foundkey = False

		# This is a nasty hack
		self.r2 = r2
		self.r3 = r3

		# Spin up the database for flag #2
		self.ICanHazDatabase()

	def write(self, msg, nl="\r\n"):
		"""
		Writes a message to the user user.
		"""

		if self.debug:
			c = 'DEBG'
		else:
			c = self.cipher
		print "%s/%s> %s" % (self.ip, c, msg)
		sys.stdout.flush()

		if self.debug:
			return self.writeClear("%s%s" % (msg, nl))
		elif self.cipher == 'ARC4':
			return self.writeARC4("%s%s" % (msg, nl))
		elif self.cipher == 'XOR':
			return self.writeXOR("%s%s" % (msg, nl))
		elif self.cipher == 'NONE':
			return self.writeClear("%s%s" % (msg, nl))

	def grue(self):
		if self.naughtycount > MAX_NAUGHTY:
			self.write("Too late, you spot the pair of glowing eye's in the darkness. The grue leaps")
			self.write("and devours you with its slavering fangs.")
			self.write("")
			self.write("You really wish you had learnt how to use apostrophes correctly.")
			self.write("")
			raise ParseError
		elif self.naughtycount > TILT_NAUGHTY:
			self.write("It is pitch black. You are likely to be eaten by a grue.")
			self.write("")
		elif self.naughtycount == TILT_NAUGHTY:
			self.write("The lights suddenly go out. It is pitch black. You are likely to be eaten by a grue.")
			self.write("")
		
	def prompt(self):
		self.grue()
		if self.naughtycount >= TILT_NAUGHTY:
			self.write("TILT -> ", nl="")
		else:
			self.write("     -> ", nl="")

	def writeClear(self, msg):
		"""
		Writes a message directly to the user (no crypto)
		"""
		try:
			self.sock.send(msg)
		except socket.error:
			# Close the connection, something went wrong
			raise ParseError

	def writeARC4(self, msg):
		"""
		Writes a message to the user encoded in ARC4.
		"""
		return self.writeClear(self.cipher_outp.encrypt(msg))

	def writeXOR(self, msg):
		"""
		Writes a message to the user encoded in repeating-key XOR.
		"""
		# pass
		return self.writeClear(msg)

	def cipherChange(self, algorithm, pw="awesomekey"):
		if algorithm == self.cipher:
			return
		elif algorithm == 'ARC4-1':
			self.key = 'murphy'
			self.cipher = 'ARC4'
			self.cipher_inp = ARC4.new(self.key)
			self.cipher_outp = ARC4.new(self.key)
			cc = 'cipherchange:cipher=ARC4:keylen=%d:charset=alpha' % (len(self.key))
		elif algorithm == 'ARC4-2':
			self.key = pw
			self.cipher = 'ARC4'
			self.cipher_inp = ARC4.new(self.key)
			self.cipher_outp = ARC4.new(self.key)
			cc = 'cipherchange:cipher=ARC4:keylen=%d:charset=alpha' % (len(self.key))
		elif algorithm == 'XOR':
			self.cipher = 'XOR'
			cc = 'cipherchange:cipher=XOR:keylen=128'
		elif algorithm == 'NONE':
			self.cipher = 'NONE'
			cc = 'cipherchange:cipher=NONE:keylen=0'
		else:
			raise CryptoError("Cipher %s unknown" % (algorithm))

		print "%s/NONE> %s" % (self.ip, cc)
		sys.stdout.flush()
		self.writeClear(cc + "\r\n")

	def enterRoom(self, r):
		"""
		Places the user in the requested room, and prints the room description.
		"""
		self.lookingAt = r
		self.write(r.entry())

		if self.post:
			self.write(random.choice(self.post))
			self.write("")

	def getRoom(self):
		i = self.lookingAt
		while i.parent != None:
			i = i.parent

		return i

	def handleInput(self, inp):
		"""
		Process user commands
		"""
		if self.debug:
			c = 'DEBG'
		else:
			c = self.cipher
		print "%s/%s <%s" % (self.ip, c, inp)
		sys.stdout.flush()

		# Hook for out-of-flow async callbacks
		if self.inputcallback:
			f = self.inputcallback
			self.inputcallback = None
			return f(self, inp)

		self.write("")

		# Look commands without an object get the room description
		if inp in Object.look_commands:
			self.enterRoom(self.getRoom())
			return

		# Other commands without an object get a hint
		if inp in Object.get_commands or inp in Object.use_commands:
			self.write("%s what?" % inp.capitalize())
			self.write("")
			self.prompt()
			return

		# Otherwise, try breaking the input up, eg. 'look at the desk' =>
		# 'look', 'desk'
		inp_list = inp.split(' ')

		# Pull out the object and commands 
		command = inp_list[0]
		obj = inp_list[-1]

		# A look command and an object of 'around' or similar is same as a look
		# without an object
		if command in Object.look_commands and obj in ['around', 'room', 'about']:
			self.enterRoom(self.getRoom())
			self.prompt()
			return

		# Commands without an object (except the above) get an error
		if len(inp) == 1:
			self.naughtycount += 1
			self.write("What?")
			self.write("")
			self.prompt()
			return

		# Resolve the object

		# Check the inventory first
		if obj in self.inventory.keys():
			self.inventory[obj].interact(obj, command, self)
			self.prompt()
			return

		# Start in the most specific namespace - the thing we're looking at -
		# and work back up the chain of parents to the room, to find what the
		# user's talking about
		i = self.lookingAt
		while i:
			if obj in i.objects.keys():
				self.lookingAt = i.objects[obj]

				i.objects[obj].interact(obj, command, self)
				self.prompt()
				return
			else:
				i = i.parent
				
		# Valid command but the object is unknown
		self.naughtycount += 1
		self.write("A %s? What's that?" % (obj))
		self.write("")
		self.prompt()

	def addInventory(self, name, obj):
		try:
			if obj.ongetcallback:
				# The callback returns true/false to determine whether the inventory add succeeds
				if obj.ongetcallback(obj, name, self):
					self.inventory[name] = obj
					return True
				else:
					return False
			else:
				self.inventory[name] = obj
				return True
			
		except Exception, e:
			# Perhaps don't crash the server if something goes wrong
			print "Server: Exception ongetcallback for %s: %s" % (name, e)
			return False


	def addPost(self, string):
		"""Adds a post-string. One of these is randomly shown every time the
		user enters a room."""
		self.post.append(string)

	def ICanHazDatabase(self):
		"""
		Creates an in-memory SQLite database for use in flag #2
		"""
		self.db_conn = sqlite3.connect(':memory:')
		self.db = self.db_conn.cursor()
		
		# Table name not a dictionary word, harder to guess
		self.db.execute("CREATE TABLE passwordz (id int, password text, username text)")
		self.db.execute("INSERT INTO passwordz VALUES (1, 'helloookitty', 'Dade \"Flagtwo\" Murphy')")
		self.db_conn.commit()

		return self.db
	
	def adminPasswordPrompt(self, p):
		"""
		Prompt for a password - extra secure version
		"""
		try:
			self.db.execute("SELECT username FROM passwordz WHERE password = '%s'" % (p))
		except (sqlite3.OperationalError, sqlite3.Warning), e:
			# Print any errors for debugging
			self.write(e)
			raise ParseError

		response = self.db.fetchone()
		if response:
			self.write("")
			self.write("Admin authorised: %s" % (response))
			self.write("")
		else:
			raise ParseError
		
	def checkInput(self, s):
		"""
		Retrieve input and sanitise
		"""
		try:
			inp_c = s.recvfrom(1024)[0]
		except socket.error:
			# Something went wrong, close the connection
			raise ParseError

		if len(inp_c) > 1023:
			raise ParseError

		if self.cipher == 'NONE' or self.debug:
			inp = inp_c
		elif self.cipher == 'ARC4':
			inp = self.cipher_inp.decrypt(inp_c)
		else:
			print "Server: Cipher not implemented! FIXME"
			raise CryptoError

		inp = inp.strip()

		validchars = string.ascii_letters + string.digits + " ,!@#$%^&*()_+-={}[]|:\";'<>?,." # ALL THE SYMBOLS \o/ except slashes, because I'm not crazy
		if not all(c in validchars for c in inp):
			print "Server: Client sent invalid characters: ",
			for c in inp:
				print "%02x " % (ord(c)), 
			print
			sys.stdout.flush()
			raise ParseError

		return inp



def handleWelcome(s, debug=False):
	global users

	u = User(s, 'NONE', debug);

	u.cipherChange('NONE')
	u.write("WeLcOmE to NSA Telepresence");
	u.write("Remember, if you die in the game, you die in real life");
	u.write("");
	u.write("Repeated authentication failures will result in deployment of tactical response.");
	u.write("");
	u.write("Enter your username");
	u.inputcallback = handleWelcome_usernamecallback
	
	return u

def handleWelcome_usernamecallback(u, username):
	"""
	Callback registered on user object when we're waiting for the username to
	be entered
	"""

	# Usernames must be reasonable
	if len(username) < 1:
		raise ParseError

	u.username = username

	# Otherwise switch to the appropriate algo
	u.write("Enter your password");
	u.inputcallback = handleWelcome_passwordcallback

	return u

def handleWelcome_passwordcallback(u, password):
	"""
	Callback registered in user object when we're waiting for the password to
	be entered
	"""
	u.password = password
	if u.username == 'admin':
		u.adminPasswordPrompt(password)
		# Password is all good, change the cipher/key
		u.cipherChange('ARC4-2', pw=u.password)
	else:
		u.cipherChange('ARC4-1')

		if password != 'murphy':
			# This output will be encrypted to permit bruteforce
			u.write("Invalid password")
			raise ParseError

	u.write("")
	u.write("Welcome %s!" % u.username)
	u.write("")
	if u.username != 'admin':
		u.write("Flag 1: The only way to win is not to play \o/")
		u.write("")

	u.enterRoom(room_start)
	u.prompt()

	return u

def closeWithError(s):
	# This must be able to handle writing to a closed socket
	try:
		s.send('error::')
	except socket.error, e:
		print "Server: Aborting socket connection: %s" % (e)
		sys.stdout.flush()
	else:
		print "Server: Closing client connection with error."
		sys.stdout.flush()
	
	try:
		s.close()
	except:
		print "Server: Exception trying close socket (already closed?)"
		sys.stdout.flush()

def init():
	debug = False
	if debug:
		debugServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		debugServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		debugServer.bind(('', 4444))
		debugServer.listen(5)

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind(('', 4445))
	server.listen(5)

	print "Server: Listening on port 4445"
	if debug:
		print "Server: and 4444 (debug)"
	sys.stdout.flush()

	socklist = [server]
	if debug:
		socklist.append(debugServer)
	users = {}

	while True:
		readers, writers, errorrrrers = select.select(socklist, [], [], 5)

		for s in readers:
			if s == server:
				(newsock, addr) = s.accept()
				print "Server: Accepting from %s:%d" % addr # (remoteaddr, port)
				sys.stdout.flush()

				try:
					newuser = handleWelcome(newsock)
				except ParseError:
					closeWithError(newsock)
					continue

				users[newsock] = newuser
				socklist.append(newsock)

			elif debug and s == debugServer:
				(newsock, addr) = s.accept()
				print "Server: Accepting debug connection from %s:%d" % addr # (remoteaddr, port)
				sys.stdout.flush()

				try:
					newuser = handleWelcome(newsock, debug=True)
				except ParseError:
					closeWithError(newsock)
					continue

				users[newsock] = newuser
				socklist.append(newsock)

			else:
				try:
					u = users[s]
					inp = u.checkInput(s)
					u.handleInput(inp)
				except (CryptoError, ParseError) as e:
					closeWithError(s)
					# Remove s from socklist, we just closed it
					socklist = [x for x in socklist if x != s]
					continue


if __name__=='__main__':
	init()

