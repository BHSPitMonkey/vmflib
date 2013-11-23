"""

Classes for dealing with brushes.

"""

from vmflib import types, vmf


class Solid(vmf.VmfClass):

    """A class representing a single brush in a map.

    You will need to create some Side objects and add them as children
    to your Solid instance. Without Sides (at least four), the brush
    will be invalid.

    """

    vmf_class_name = 'solid'
    solid_count = 0

    def __init__(self):
        vmf.VmfClass.__init__(self)
        self.auto_properties = []

        self.properties['id'] = Solid.solid_count
        Solid.solid_count += 1


class Side(vmf.VmfClass):

    """A class representing a single side of a brush."""

    vmf_class_name = 'side'
    side_count = 0

    def __init__(self, plane=types.Plane(), material='BRICK/BRICKFLOOR001A'):
        vmf.VmfClass.__init__(self)
        self.plane = plane
        self.material = material
        self.rotation = 0
        self.lightmapscale = 16
        self.smoothing_groups = 0
        self.uaxis = types.Axis()
        self.vaxis = types.Axis()

        self.auto_properties = ['plane', 'material', 'uaxis', 'vaxis',
            'rotation', 'lightmapscale', 'smoothing_groups']

        p = self.properties
        p['id'] = Solid.solid_count
        Solid.solid_count += 1


class Group(vmf.VmfClass):

    """A class representing a group of brushes."""

    vmf_class_name = 'group'
    group_count = 0

    def __init__(self):
        vmf.VmfClass.__init__(self)
        self.auto_properties = []

        self.properties['id'] = Group.group_count
        Group.group_count += 1


class DispInfo(vmf.VmfClass):

    """A class for holding displacement map info in a Side."""

    vmf_class_name = 'dispinfo'

    def __init__(self, power, normals, distances):
        vmf.VmfClass.__init__(self)
        self.power = power
        self.startposition = "[0 0 0]"
        self.elevation = 0
        self.subdiv = 0
        self.normals = Normals(power, normals)
        self.distances = Distances(power, distances)
        self.offsets = Offsets(power)
        self.offset_normals = OffsetNormals(power)
        self.alphas = Alphas(power)
        self.triangle_tags = TriangleTags(power)
        self.allowed_verts = AllowedVerts(power)

        self.auto_properties = ['power', 'startposition', 'elevation', 'subdiv']
        self.children.extend([self.normals, self.distances, self.offsets,
        self.offset_normals, self.alphas, self.triangle_tags, 
        self.allowed_verts])

    def set_power(self, power):
        self.power = power
        

class Normals(vmf.VmfClass):
    
    """
    
    You should feed this thing a 2-dimensional list of Vertex values, with
    (2**power)+1 rows and columns. Perform all your operations on this list
    before initializing this Normals object, rather than trying to mutate this
    object afterwards.
    
    """
    vmf_class_name = 'normals'

    def __init__(self, power, values):
        vmf.VmfClass.__init__(self)
        #self.values = values
        
        for i in range(2**power + 1):
            row_string = ''
            for vert in values[i]:
                row_string += "%d %d %d " % (vert.x, vert.y, vert.z)
            self.properties["row%d" % i] = row_string[:-1]


class Distances(vmf.VmfClass):
    vmf_class_name = 'distances'

    def __init__(self, power, values):
        vmf.VmfClass.__init__(self)
        
        self.values = values
        
        for i in range(2**power + 1):
            row_string = ''
            for distance in values[i]:
                row_string += "%d " % distance
            self.properties["row%d" % i] = row_string[:-1]


class Offsets(vmf.VmfClass):
    vmf_class_name = 'offsets'

    def __init__(self, power):
        vmf.VmfClass.__init__(self)


class OffsetNormals(vmf.VmfClass):
    vmf_class_name = 'offset_normals'

    def __init__(self, power):
        vmf.VmfClass.__init__(self)


class Alphas(vmf.VmfClass):
    vmf_class_name = 'alphas'

    def __init__(self, power):
        vmf.VmfClass.__init__(self)


class TriangleTags(vmf.VmfClass):
    vmf_class_name = 'triangle_tags'

    def __init__(self, power):
        vmf.VmfClass.__init__(self)


class AllowedVerts(vmf.VmfClass):
    vmf_class_name = 'allowed_verts'

    def __init__(self, power):
        vmf.VmfClass.__init__(self)
