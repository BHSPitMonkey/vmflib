"""

Classes representing some of the data types that are used when giving
property values in a VMF map.

"""


class Vertex:

    """An XYZ location given by 3 decimal values."""

    def __init__(self, x=0, y=0, z=0):
        """Create a new Vertex representing the position (x, y, z)."""
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return '(%s %s %s)' % (self.x, self.y, self.z)


class RGB:

    """A color given by 3 integer values separated by spaces (0-255)."""

    def __init__(self, r=0, g=0, b=0):
        """Create a new RGB color."""
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)

    def __repr__(self):
        return '%d %d %d' % (self.r, self.g, self.b)


class Bool:

    """A boolean value rendered as a 0 or 1."""

    def __init__(self, state=False):
        """Create a new Bool with the specified state."""
        self.state = state

    def __repr__(self):
        return str(int(bool(self.state)))


class Plane:

    """A set of three Vertices which define a plane."""

    def __init__(self, v0=Vertex(), v1=Vertex(), v2=Vertex()):
        """Create a new Vertex representing the position (x, y, z)."""
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2

    def __repr__(self):
        return '%s %s %s' % (self.v0, self.v1, self.v2)
