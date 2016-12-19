"""
Contemporary Loft Demo
Version: 1.12.39

Keywords: ['grabbing', 'video', 'architecture', 'sound', 'apartment',
			'residential']
"""

# Import modules.
import random

import viz
import vizfx
import vizact
import vizconnect

import tools


# We're going to add a grabber with highlighting, so we have to update stencil
# settings before calling viz.go
if __name__ == "__main__":
	viz.setOption('viz.display.stencil', 8)

# Add the local events (events specific to this demo)
vizconnect.go('vizconnect_config_local_events.py')

# get the quality setting of the demo if specified
DEMO_QUALITY_SETTING = max(0, viz.getOption('DEMO_QUALITY_SETTING', default=4, type=int))

vizfx.addPointLight(pos=(0, 5, 1, 0), euler=(0, 90, 0))

# Load the vizconnect configuration.
if __name__ == "__main__":
	vizconnect.go('./vizconnect_config.py')
	viz.setMultiSample(DEMO_QUALITY_SETTING*2)
	# disable the head lamps since we're doing lighting ourselves
	for window in viz.getWindowList():
		window.getView().getHeadLight().disable()
else:
	vizconnect.go('./multiscript_vizconnect_config.py')

# Add a viewpoint so the user starts at [0, 0, 0].
vp = vizconnect.addViewpoint(pos=[0, 0, 0])

scenario= ['art/Domus_Guitar_Brendan.osgb', 'art/Domus_Guitar_Zach.osgb', 'art/Domus_Guitar_Rob.osgb']
choice= random.randint(0,2)
print(choice)

# Load the model for the room.
room = viz.addChild(scenario[choice])
room.hint(viz.OPTIMIZE_INTERSECT_HINT)

# Add a video to play it on each TV.
media = viz.addVideo('art/cartoon-bird.wmv')

# Get the handles to the TV objects in the living room, the main bedroom and the kid's room,
# and apply video texture to the objects.
TVscreen1 = room.getChild('SL_TV Screen')
TVscreen1.texture(media)

TVscreen2 = room.getChild('Object03x')
TVscreen2.texture(media)

TVscreen3 = room.getChild('TV screen Suite')
TVscreen3.texture(media)


drawer = room.getChild('Drawer')
pillow1= room.getChild('Cushion')
pillow2= room.getChild('Cushion2')

#Conditional
if choice== 0 or 1:
	movable_Drive= room.getChild('Movable_Drive')

if choice== 1:
	pillow3= room.getChild('Cushion3')
	pillow4= room.getChild('Cushion4')
	pillow5= room.getChild('Cushion5')


# Play the video on a continuous loop.
media.play()
media.loop()

# Get description dictionary.
descriptions = room.getDescriptionDict()

# Iterate through the description dictionary and add nodes with grab=true to
# a list of grabbable items. Get handles to the guitars for later

#Conditional
if choice== 0 or 2:
	grabbableItems = [drawer, pillow1, pillow2]
else:
	grabbableItems = [drawer, pillow1, pillow2, pillow3, pillow4, pillow5]


leftGuitar = None
rightGuitar = None


inspectorPlacer = tools.placer.Inspection()
for node, desc in descriptions.iteritems():
	if 'grab=true' in desc[0].lower():
		room.getChild(node+'-GEODE').disable(viz.INTERSECTION)
		parent = room.insertGroupAbove(node+'-GEODE')
		parent.disable(viz.INTERSECTION)
		grabbableItems.append(parent)
		# Get handles to the guitars
		if node == 'Guitarra vermelha':
			leftGuitar = parent
			leftGuitar.VIZ_TOOL_PLACER = inspectorPlacer
		if node == 'DEC_Gruitarra 01':
			rightGuitar = parent
			rightGuitar.VIZ_TOOL_PLACER = inspectorPlacer


def onGuitarGrab(e):
	"""What happens when one of the guitars is grabbed"""
	if e.grabbed == leftGuitar or e.grabbed == rightGuitar:
		choice = random.choice(guitarGrabSounds)
		choice.stop()
		choice.play()


def onGuitarRelease(e):
	"""What happens when one of the guitars is released"""
	if e.released == leftGuitar or e.released == rightGuitar:
		choice = random.choice(guitarReleaseSounds)
		choice.stop()
		choice.play()

	threshold = 0.25

	
	if e.released == leftGuitar:
		xDisplacement = abs(leftGuitar.getPosition()[0])
		yDisplacement = abs(leftGuitar.getPosition()[1])
		if xDisplacement < threshold and yDisplacement < threshold:
			leftGuitar.setPosition(0, 0, 0)
			leftGuitar.setEuler(0, 0, 0)
	
	if e.released == rightGuitar:
		xDisplacement = abs(rightGuitar.getPosition()[0])
		yDisplacement = abs(rightGuitar.getPosition()[1])
		if xDisplacement < threshold and yDisplacement < threshold:
			rightGuitar.setPosition(0, 0, 0)
			rightGuitar.setEuler(0, 0, 0)

#needs to move the flash drive as well, only if one is there
def onDrawerRelease(e):
	threshold2 = 5.00
	if e.released == drawer:
		xDisplacement = abs(drawer.getPosition()[0])
		yDisplacement = abs(drawer.getPosition()[1])
		if xDisplacement < threshold2 or yDisplacement < threshold2:
			drawer.setPosition(.57, 0, 0)
			drawer.setEuler(0, 0, 0)
			if choice== 0 or 1:
				movable_Drive.setPosition(.57, 0, 0)

	
# Setup callback to enable guitar sounds
vizact.onevent(viz.getEventID('GRABBER_GRAB_EVENT'), lambda e: (True, e), onGuitarGrab)
vizact.onevent(viz.getEventID('GRABBER_RELEASE_EVENT'), lambda e: (True, e), onGuitarRelease)
vizact.onevent(viz.getEventID('GRABBER_RELEASE_EVENT'), lambda e: (True, e), onDrawerRelease)

# Manually add a few additional items to the grabbable list, which were not added above by the description parser
extraGrabbables = [	'DEC_Vaso Ovo', 				# Cellular-egg decorative vase
					'arch49_055_obj_00', 			# Orange ball cap on child's bed
					'DEC_Fruteira B01',				# Basket of lemons on kitchen counter
					'DEC_fruteiras_A_01_maca_08',	# Basket of apples on kitchen counter
					'DEC_vaso', 					# Toilet in master bedroom
					'DEC_vaso02',					# Toilet in common area
					'Pot',]							# Pot on kitchen counter
					

for name in extraGrabbables:
	room.getChild(name+'-GEODE').disable(viz.INTERSECTION)
	parent = room.insertGroupAbove(name+'-GEODE')
	parent.disable(viz.INTERSECTION)
	grabbableItems.append(parent)




# Add a sound to indicate the layout has been reset
resetSound = viz.add('art/sounds/demo_reset.wav')
resetSound.stop()

# Add alternate floor, and get the floor in the existing model
tileFloor = viz.add('art/tile_floor.osgb')
tileFloor.visible(viz.OFF)
hardwoodFloor = room.getChild('Piso Sala_Alt-wood')


def changeFlooring():
	"""Toggles between showing one or the other of the two floors"""
	if tileFloor.getVisible():
		tileFloor.visible(viz.OFF)
		hardwoodFloor.visible(viz.ON)
	else:
		tileFloor.visible(viz.ON)
		hardwoodFloor.visible(viz.OFF)



# Setup callback to switch the floor type
vizact.onevent(viz.getEventID('CHANGE_FLOORING'), lambda e: (True, None), changeFlooring)


def resetMovedObjects(playAudio=True):
	"""Function to place the moved objects back into their initial positions"""
	if playAudio:
		resetSound.stop()
		resetSound.play()
	for item in grabbableItems:
		item.setPosition(0, 0, 0)
		item.setEuler(0, 0, 0)


def init():
	"""Code for one time initialization routine."""
	# add grabber tools based on proxy tools
	for proxyWrapper in vizconnect.getToolsWithMode('Proxy'):
		grabberTool = tools.grabber.HandGrabber(usingPhysics=False,
												usingSprings=False,
												placementMode=tools.placer.MODE_DROP_DOWN)
		
		name = 'grabber_tool_based_on_'+proxyWrapper.getName()
		grabberWrapper = vizconnect.addTool(raw=grabberTool,
											name=name,
											make='Virtual',
											model='Grabber')
		# parent the grabber wrapper to the proxy's parent
		grabberWrapper.setParent(proxyWrapper)
		
		grabberTool.setItems(grabbableItems)
	
	viz.callback(viz.getEventID('RESET_THE_LOFT_LAYOUT'), lambda e: resetMovedObjects())


def show():
	"""Function used to add/show/enable non vizard resources. This is
	necessary to supply context switching between multiple, demos or scripts.
	"""
	for proxyWrapper in vizconnect.getToolsWithMode('Proxy'):
		grabberTool = vizconnect.getTool('grabber_tool_based_on_'+proxyWrapper.getName()).getRaw()
		# for proxies: set obj, function, action index
		proxyWrapper.getRaw().setCallback(grabberTool, grabberTool.grabAndHold, 1)
	vp.add(vizconnect.getDisplay())
	resetMovedObjects(playAudio=False)


def hide():
	"""Function used to remove/hide/disable non vizard resources. This is
	necessary to supply context switching between multiple, demos or scripts.
	"""
	for proxyWrapper in vizconnect.getToolsWithMode('Proxy'):
		proxyWrapper.getRaw().clear()
	vp.remove(vizconnect.getDisplay())


# For the multiscript demos, show() is called automatically for each demo,
# but for running the stand-alone demo, need to call show() explicitly.
if __name__ == "__main__":
	init()
	show()
