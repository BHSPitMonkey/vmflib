"""

Main classes for working with VMF maps.

"""

from types import *


###############################################################################
### This is a base class for the VMF "Classes" we will define further down. ###
###############################################################################

class VmfClass:

    """A class representing a key-value group in the VMF KeyValues structure."""

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
            string += '%s"%s" "%s"\n' % (tab_prefix_inner,
                attr_name, getattr(self, attr_name))

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
        self.mins = Vertex(99999, 99999, 99999)
        self.maxs = Vertex(-99999, -99999, -99999)
        self.active = Bool(0)

        self.auto_properties = ['mins', 'maxs', 'active']


class Entity(VmfClass):

    """A class representing an entity class in a Valve Map."""
 
    vmf_class_name = 'entity'
    entitycount = 0

    def __init__(self, class_name, entity_type):
        VmfClass.__init__(self)
        self.classname = class_name        # Required
        self.spawnflags = 0

        self.auto_properties = ['classname', 'spawnflags']

        p = self.properties
        p['id'] = Entity.entitycount
        Entity.entitycount += 1            # Increment entity counter


class Connections(VmfClass):

    """Represents a connections class for use within an Entity object.
    
    Give this class properties with values of type Output (types.Output).
    
    """

    vmf_class_name = "connections"


class World(Entity):

    """A class representing the world section of a Valve Map.

    Be sure to create lots of brush (Solid) objects and add them to the World
    object's children attribute. Nobody likes an empty world.

    """

    vmf_class_name = "world"
    worldcount = 0

    def __init__(self):
        Entity.__init__(self, 'worldspawn', 'TODO')
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

    def __init__(self):
        VmfClass.__init__(self)            # Superclass initializer

        # These properties are objects that represent the basic structure
        # of a Valve Map.  Some of these are meant to contain many
        # additional children, comprising all the polygons and props in the
        # level.
        #self.versioninfo = VersionInfo()
        #self.visgroups = VisGroups()
        self.world = World()
        #self.hidden = 0
        self.cameras = Cameras()
        self.cordon = Cordon()

        # Push these properties (references) into our children list
        c = self.children
        #c.append(self.versioninfo)
        #c.append(self.visgroups)
        c.append(self.world)
        #c.append(self.hidden)
        c.append(self.cameras)
        c.append(self.cordon)

    def write_vmf(self, filename):
        """Write the map to a file in VMF format."""
        print 'Writing to: ' + filename
        f = open(filename, 'w')
        f.write(repr(self))
        f.close()
