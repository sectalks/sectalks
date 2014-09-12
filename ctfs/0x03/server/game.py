#
# sectalks 0x03 challenge server
#
# This file defines the  game world: Object and Room instances are created and
# assigned relationships to each other. 
#

import os.path
import socket
import struct

from classes import Room, Object

r = Room(
			"""You are standing in front of a desk in a quiet, windowless office.

			There are posters on the walls. The office door is closed. There is
			a faint smell of tuna.""",
		)

room_start = r


poster = Object(
			"""It seems to be some sort of comic. Two people are talking:
			
			-- Wow - engines can burn vegetable oil!
			-- Well, sure. You can burn almost any organic matter. Corns, leaves, spices...
			-- Spices? Really?
			-- Sure - Mussolini made the trains run on thyme.
			-- ... We are no longer friends

			You assume this is supposed to be funny. """,
			)

r.addObject(['poster', 'posters'], poster)

door = Object(
			"""The door is heavy and imposing. And slightly too short. What
			kind of organisation would build a doorway too short?

			You try and turn the handle but the door is unfortunately also
			locked. There's a promising looking keyhole, but your lockpicks
			must have fallen out of your pocket at some point in the recent
			past. Bummer. 

			Here's hoping a fire doesn't break out, or you'll be screwed. You
			should report these guys for a code violation or something.""",
			)

r.addObject(['doorway', 'door', 'exit'], door)

tunasmell = Object(
			"""You look around but you can't work out where the smell is coming
			from. It's getting pretty bad in here.  """,
			)

r.addObject(['tuna', 'smell'], tunasmell)

desk = Object(
			"""A large wooden desk sits in the centre of the room. It's
			imposing: you could imagine sitting begin it, stroking your feline
			companion as you plot world domination. 

			Unfortunately, there's no chair. There is however a rubbish bin and
			a shredder tucked under the desk, you didn't see them before.
			
			There is a folder of documents on the desk.""", 
		)

r.addObject(['desk', 'table'], desk)

chair = Object(
			"""You sit down behind the desk in the invisible chair.
			
			It's really pretty comfortable. But slightly unnerving.""",
			)

r.addObject(['chair', 'seat'], chair)

rbin = Object(
			"""The bin contains some crumpled documents, along with a
			half-eaten tuna sandwich. The sandwich looks pretty nasty.

			At least you know where the awful smell is coming from now.""",
			)

desk.addObject(['bin', 'rubbish', 'rubbishbin'], rbin)

sandwich = Object(
			"""The sandwich is pretty nasty. It makes moist, squishy noises as
			you poke it.""",
			)

rbin.addObject(['sandwich', 'tunasandwich', 'tuna'], sandwich)

documents = Object(
			"""Unfortunately, the documents are too stained in tuna juice to
			read.""",
			)

rbin.addObject(['documents', 'paper', 'papers'], documents)

shredder = Object(
			"""Under the desk sits an industrial-sized shredder. The intake is
			enormous, you could fit a whole sandwich in here!""",
			)

key = Object(
			"""It's a fancy old-fashioned key. You guess it's just as secure as
			a swipecard, right? Given that you don't have any lockpicks on you."""
			)

def checkFoundKey(obj, name, user):
	"""
	Only permits key pickup when user.foundkey == True
	"""
	return user.foundkey

key.ongetcallback = checkFoundKey

desk.addObject(['key', 'oldfashionedkey', 'oldkey', 'lockpick', 'lockpicks'], key)

# Add the openDoor action to the door, which is attached to the room object
def openDoor(user):
	user.write("The key easily opens the door, which swings open with an ominous ")
	user.write("creak. As you step through, it clicks shut behind you and disappears ")
	user.write("perfectly into the wall.")
	user.write("")
	user.write("You're not going to be able to go back that way.")
	user.write("")
	user.enterRoom(user.r2)

door.actions[key] = openDoor

folder = Object(
			"""The folder looks pretty important. It's got "TOP SECERT" written
			on the front in red marker.

			This doesn't seem all that professional.""",
			)

def canHazFiletimes(obj, name, user):
	"""
	Dumps a file down to the user. Modifies the desk object to reveal the key
	"""
	filename = "folder.ppt"

	size = os.path.getsize(filename)
	f = open(filename, "r")

	user.write("filetransfer:length=%d:folder.ppt" % (size))
	# Write in 1000 byte chunks 
	for c in iter(lambda: f.read(1000), ''): # lambda functions are fun! \o/ also iterables
		user.write(c, nl='')

	user.write("")
	user.write("Moving the folder, you notice a key tucked underneath.")
	user.foundkey = True

	return True

folder.ongetcallback = canHazFiletimes
folder.hardtoget = True
desk.addObject(['folder', 'folders', 'documents'], folder)

def coveredInTuna(user):
	user.write(
			"""The shredder fires up and sucks in the sandwich. As the sandwich\r\nexplodes, you realise your mistake. The tuna sprays everywhere. \r\nThis is going to be a nightmare to clean.""")
	user.write("")

	user.addPost("Your clothes smell powerfully of tuna.")
	user.addPost("Tuna juice drips on to the floor as you move.")
	user.addPost("You brush a piece of tuna out of your hair.")
	user.addPost("The powerful reek of rotten tuna is inescapable.")

shredder.addAction(sandwich, coveredInTuna)

desk.addObject(['shredder'], shredder)

r2 = Room(
			"""You are standing in a small passageway. At the other end is a
			door.""",
		)


door = Object(
			"""You walk over to the door. There's a sign on it the reads CELLAR.""",
			)
r2.addObject(['door'], door)

r3 = Room(
			"""You're standing in a dimly lit basement room. 

			The stairs behind you have completely collapsed; you're not going
			back that way in a hurry.

			At least there's a toilet down here.""",
		)

def openCellarDoor(obj, name, command, user):
	user.write("The handle turns easily in your hand and you step through into")
	user.write("darkness.")
	user.write("")
	user.write("As you take a couple of steps forward, the crumbling wooden")
	user.write("stairs under your feet give way. You grab the handrail but ")
	user.write("it doesn't help much as you fall towards the concrete floor ")
	user.write("below, landing hard amidst a pile of rotten wood and dust.")
	user.write("")
	user.write("Luckily, you seem to be ok, except for a few bruises.")
	user.write("")

	user.enterRoom(user.r3)

door.cmd_hooks['open'] = openCellarDoor

stairs = Object(
			"""The stairs have completely collapsed. There's a good five
			vertical metres of sheer, smooth concrete wall between you and the
			doorway far above.
			
			There don't seem to be any other exits."""
			)
r3.addObject(['stair', 'stairs', 'exit', 'door', 'doorway'], stairs)

light = Object(
			"""A single bulb swings slowly in the centre of the room, and does
			a pretty terrible job of illuminating anything. There's just enough
			light to see so you don't walk into things."""
			)
r3.addObject(['light', 'switch', 'lightswitch'], light)

toilet = Object(
			"""The toilet door has a sign on it marked OUT OF ORDER. Great.
			
			As you cautiously push open the door, you notice there's a filing
			cabinet stuck in here."""
			)
r3.addObject(['toilet', 'lavatory'], toilet)

filingcab = Object(
			"""There's another sign stuck to the filing cabinet: BEWARE OF THE
			LEOPARD.

			The cabinet seems to be locked, but the bottom drawer looks like it
			might open if you pull hard enough. """
			)
toilet.addObject(['cabinet', 'filing', 'cabinet', 'filingcabinet'], filingcab)

drawer = Object(
			"""You pull open the drawer with some effort. There's a radio in
			here! It seems to be playing some sort of golden hits station.

			You can listen to it if you want."""
			)
filingcab.addObject(['drawer', 'bottom', 'bottomdrawer', 'radio'], drawer)

def playTheThing(obj, name, command, user):
	user.cipherChange("NONE")
	user.write("SDP:")
	user.write("v=0")
	user.write("o=- 0 0 IN IP4 127.0.0.1")
	user.write("s=Helloooooo! I've just got to let you knooooowwww")
	user.write("c=IN IP4 127.0.0.1")
	user.write("t=0 0")
	user.write("a=tool:l33tencoder 53.21.1")
	user.write("m=audio 4445 RAW 0")

	# Do the thing! \o/
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.bind(('localhost', 55555))

		# Write 1500x max-1000 byte chunks - note this is synchronous and so we want to limit how long it writes for
		for i in range(1500):
			p = s.recvfrom(1024)[0]
			user.write(p, nl='')
		s.close()
	except socket.error, e:
		print "Server: Error opening streaming socket: %s" % (e)

	user.cipherChange("ARC4-2", pw=user.password)

drawer.cmd_hooks['listen'] = playTheThing

#r.addObject(['rosebud'], drawer)

