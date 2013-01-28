"""

Classes for dealing with brushes.

"""

from vmf import VmfClass
from types import *


class Solid(VmfClass):

    """A class representing a single brush in a map.

    You will need to create some Side objects and add them as children
    to your Solid instance. Without Sides (at least four), the brush
    will be invalid.

    """

    vmf_class_name = 'solid'
    solid_count = 0

    def __init__(self):
        VmfClass.__init__(self)
        self.auto_properties = []

        self.properties['id'] = Solid.solid_count
        Solid.solid_count += 1


class Side(VmfClass):

    """A class representing a single side of a brush."""

    vmf_class_name = 'side'
    side_count = 0

    def __init__(self, plane=Plane(), material='BRICK/BRICKFLOOR001A'):
        VmfClass.__init__(self)
        self.plane = plane
        self.material = material
        self.uaxis = '[1 0 0 0] 0.25'
        self.vaxis = '[0 0 -1 0] 0.25'
        self.rotation = 0
        self.lightmapscale = 16
        self.smoothing_groups = 0

        self.auto_properties = ['plane', 'material', 'uaxis', 'vaxis',
            'rotation', 'lightmapscale', 'smoothing_groups']

        p = self.properties
        p['id'] = Solid.solid_count
        Solid.solid_count += 1


class Group(VmfClass):

    """A class representing a group of brushes."""
    
    vmf_class_name = 'group'
    group_count = 0

    def __init__(self):
        VmfClass.__init__(self)
        self.auto_properties = []

        self.properties['id'] = Group.group_count
        Group.group_count += 1
