# map.py
# Package: vmflib
# Author: Stephen Eisenhauer (mail@stepheneisenhauer.com)
# 
# Represents a map using VMF (Valve Map Format).
# Can be created/manipulated using Python interfaces, then exported
# as a VMF file (plain text) to be compiled and loaded into a game.
# 
# More info:
# https://developer.valvesoftware.com/wiki/VMF_documentation
# https://developer.valvesoftware.com/wiki/VMF_documentation:_World_Class

class Group:
	"""A class representing a key-value group in the VMF KeyValues structure"""
	classname = 'UntitledClass'

	def __init__(self):
		self.properties = dict()	# Single-value properties
		self.children = []			# Sub-groups
	
	# Render this group as a string
	def tostring(self, tab_level=-1):
		string = ''
		
		# Generate line prefixes (tab characters) for later
		tab_prefix = ''
		for i in range(tab_level):
			tab_prefix += '\t'
		tab_prefix_inner = tab_prefix + '\t'
		
		
		# Generate class declaration and opening brace
		if (self.classname != False):
			string += tab_prefix + self.classname + '\n'
			string += tab_prefix + '{\n'
		
		# Print properties
		for item in self.properties.items():
			string += tab_prefix_inner + '"' + item[0] + '" "' + str(item[1]) + '"\n'
		
		# Print child groups
		for child in self.children:
			string += child.tostring(tab_level+1)
		
		# Print close brace
		if (self.classname != False):
			string += tab_prefix + '}\n'
		
		return string

########################################################################
### These classes define the various "Classes" (groups) found in a   ###
### VMF map. They derive from the Group class.                       ###
########################################################################

class VersionInfo(Group):
	"""A class representing the versioninfo section of a Valve Map"""
	classname = 'versioninfo'

	def __init__(self):
		Group.__init__(self)			# Call superclass initializer
		
		p = self.properties
		p['editorversion'] = 0
		p['editorbuild'] = 0
		p['mapversion'] = 0
		p['formatversion'] = 100
		p['prefab'] = 0

class VisGroups(Group):
	"""A class representing the versioninfo section of a Valve Map"""
	classname = 'visgroups'

class Cameras(Group):
	"""A class representing the cameras section of a Valve Map"""
	classname = 'cameras'

class Entity(Group):
	"""A class representing an entity class in a Valve Map"""
	classname = 'entity'
	entitycount = 0
	
	def __init__(self, class_name, entity_type):
		Group.__init__(self)			# Call superclass initializer
		
		p = self.properties
		p['id'] = Entity.entitycount
		Entity.entitycount += 1			# Increment world counter
		p['classname'] = class_name		# Must be provided
		p['spawnflags'] = 0

# Tip: After instantiating a World object, put a bunch of Solids into its children list.
class World(Entity):
	"""A class representing the world section of a Valve Map"""
	classname = "world"
	worldcount = 0

	def __init__(self):
		Entity.__init__(self, 'worldspawn', 'TODO')	# Call superclass initializer
		
		p = self.properties
		p['id'] = World.worldcount
		World.worldcount += 1			# Increment world counter
		p['mapversion'] = 0
		p['skyname'] = 'sky_day01_01'	# A default sky, available in all Source games

		
		c = self.children
		# TODO: Solid, Hidden, Group

########################################################################
### The class you'll want to use no matter what is ValveMap.         ###
### This represents the top-level map itself.                        ###
########################################################################

# Tip: After instantiating a World object, put a bunch of Entities into its children list
class ValveMap(Group):
	"""A class encapsulating the Valve Map Format (VMF)"""
	classname = False					# Document-level, has no class name
	
	
	def __init__(self):
		Group.__init__(self)				# Superclass initializer
		
		# These properties are objects that represent the basic structure
		# of a Valve Map.  Some of these are meant to contain many 
		# additional children, comprising all the polygons and props in the
		# level.
		#self.versioninfo = VersionInfo()	# TODO: Is this necessary?
		#self.visgroups = VisGroups()		# Normally stays empty
		self.world = World()
		#self.hidden = 0					# TODO: Is this necessary?
		self.cameras = Cameras()
		#self.cordon = 0					# TODO: Is this necessary?
		
		# Push these properties (references) into our children list
		c = self.children
		#c.append(self.versioninfo)
		#c.append(self.visgroups)
		c.append(self.world)
		#c.append(self.hidden)
		c.append(self.cameras)
		#c.append(self.cordon)
	
	def write_vmf(self, filename):
		print 'Writing to: ' + filename
		f = open(filename, 'w')
		f.write(self.tostring())
		f.close()
