"""

Main classes for working with VMF maps.

"""

from vmflib import types


###############################################################################
### This is a base class for the VMF "Classes" we will define further down. ###
###############################################################################

class VmfClass:

    """A class representing a KeyValue group in the VMF KeyValues structure."""

    vmf_class_name = 'UntitledClass'

    def __init__(self):
        self.properties = {}
        self.auto_properties = []
        self.children = []

    # Render this class as a string
    def __repr__(self, tab_level=-1):
        string = ''

        # Generate line prefixes (tab characters) for later
        tab_prefix = ''
        for i in range(tab_level):
            tab_prefix += '\t'
        tab_prefix_inner = tab_prefix + '\t'

        # Generate class declaration and opening brace
        if (self.vmf_class_name):
            string += tab_prefix + self.vmf_class_name + '\n'
            string += tab_prefix + '{\n'

        # Print auto properties (properties bound to instance attributes)
        for attr_name in self.auto_properties:
            value = getattr(self, attr_name)
            if value is not None:
                string += '%s"%s" "%s"\n' % (tab_prefix_inner, attr_name, value)

        # Print properties
        for item in self.properties.items():
            string += '%s"%s" "%s"\n' % (tab_prefix_inner, item[0], item[1])

        # Print child groups
        for child in self.children:
            string += child.__repr__(tab_level + 1)

        # Print close brace
        if (self.vmf_class_name):
            string += tab_prefix + '}\n'

        return string


###############################################################
### These classes define the various "Classes" found in a   ###
### VMF map. They derive from the VmfClass class.           ###
###############################################################

class VersionInfo(VmfClass):

    """A class representing the versioninfo section of a Valve Map."""

    vmf_class_name = 'versioninfo'

    def __init__(self):
        VmfClass.__init__(self)

        p = self.properties
        p['editorversion'] = 0
        p['editorbuild'] = 0
        p['mapversion'] = 0
        p['formatversion'] = 100
        p['prefab'] = 0


class VisGroups(VmfClass):

    """A class representing the versioninfo section of a Valve Map."""

    vmf_class_name = 'visgroups'


class Cameras(VmfClass):

    """A class representing the cameras section of a Valve Map."""

    vmf_class_name = 'cameras'


class Cordon(VmfClass):

    """A class representing the cordon section of a Valve Map."""

    vmf_class_name = 'cordon'

    def __init__(self):
        VmfClass.__init__(self)
        self.mins = types.Vertex(99999, 99999, 99999)
        self.maxs = types.Vertex(-99999, -99999, -99999)
        self.active = types.Bool(0)

        self.auto_properties = ['mins', 'maxs', 'active']


class Entity(VmfClass):

    """A class representing an entity class in a Valve Map."""

    vmf_class_name = 'entity'
    entitycount = 0

    def __init__(self, class_name):
        VmfClass.__init__(self)
        self.classname = class_name
        self.spawnflags = 0
        self.origin = None
        self.targetname = None

        self.auto_properties = ['classname', 'spawnflags', 'origin', 
            'targetname']

        p = self.properties
        p['id'] = Entity.entitycount
        Entity.entitycount += 1            # Increment entity counter
        
        # Add ourself to the active map
        if ValveMap.instance:
            ValveMap.instance.children.append(self)


class Connections(VmfClass):

    """Represents a connections class for use within an Entity object.
    
    This class behaves a little differently than the other VMF classes:
    Its Key-Value entries have non-unique keys, so we can't model them using
    dictionaries. This class's `children` array will contain Output objects
    and we will print them in their own special way.

    """

    vmf_class_name = "connections"

    # Render this class as a string
    def __repr__(self, tab_level=-1):
        string = ''

        # Generate line prefixes (tab characters) for later
        tab_prefix = ''
        for i in range(tab_level):
            tab_prefix += '\t'
        tab_prefix_inner = tab_prefix + '\t'

        # Generate class declaration and opening brace
        if (self.vmf_class_name):
            string += tab_prefix + self.vmf_class_name + '\n'
            string += tab_prefix + '{\n'

        # Print child groups
        for output in self.children:
            string += '%s%s\n' % (tab_prefix_inner, output)

        # Print close brace
        if (self.vmf_class_name):
            string += tab_prefix + '}\n'

        return string


class World(Entity):

    """A class representing the world section of a Valve Map.

    Be sure to create lots of brush (Solid) objects and add them to the World
    object's children attribute. Nobody likes an empty world.

    """

    vmf_class_name = "world"
    worldcount = 0

    def __init__(self):
        Entity.__init__(self, 'worldspawn')
        self.skyname = 'sky_day01_01'

        self.auto_properties += ['skyname']

        p = self.properties
        p['id'] = World.worldcount
        World.worldcount += 1
        p['mapversion'] = 0


########################################################################
### The class you'll want to use no matter what is ValveMap.         ###
### This represents the top-level map itself.                        ###
########################################################################

# Tip: After instantiating a World object, put a bunch
# of Entities into its children list
class ValveMap(VmfClass):

    """A class encapsulating the Valve Map Format (VMF)."""

    vmf_class_name = False                 # Document-level, has no class name
    instance = None                        # Singleton instance

    def __init__(self):
        VmfClass.__init__(self)            # Superclass initializer
        ValveMap.instance = self

        # These properties are objects that represent the basic structure
        # of a Valve Map.  Some of these are meant to contain many
        # additional children, comprising all the polygons and props in the
        # level.
        #self.versioninfo = VersionInfo()
        #self.visgroups = VisGroups()
        self.world = World()    # Automatically added to map
        #self.hidden = 0
        self.cameras = Cameras()
        self.cordon = Cordon()

        # Push these properties (references) into our children list
        c = self.children
        #c.append(self.versioninfo)
        #c.append(self.visgroups)
        #c.append(self.hidden)
        c.append(self.cameras)
        c.append(self.cordon)

    def write_vmf(self, filename):
        """Write the map to a file in VMF format."""
        print('Writing to: ' + filename)
        f = open(filename, 'w')
        f.write(repr(self))
        f.close()
