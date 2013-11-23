"""

Classes representing some of the data types that are used when giving
property values in a VMF map.

"""


class Vertex:

    """An XYZ location given by 3 decimal values and printed with parens."""

    def __init__(self, x=0, y=0, z=0):
        """Create a new Vertex representing the position (x, y, z)."""
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return '(%s %s %s)' % (self.x, self.y, self.z)


class Origin:

    """An XYZ location given by 3 decimal values and printed without parens."""

    def __init__(self, x=0, y=0, z=0):
        """Create a new Origin representing the position (x, y, z)."""
        if type(x) == tuple:
            self.x, self.y, self.z = x
        else:
            self.x = x
            self.y = y
            self.z = z

    def __repr__(self):
        return '%s %s %s' % (self.x, self.y, self.z)


class Axis:

    """A u-axis or v-axis value used in a Side object in a brush."""

    def __init__(self, x=0, y=0, z=0, translate=0, scale=0.25):
        """Create a new Axis value."""
        self.x = x
        self.y = y
        self.z = z
        self.translate = translate
        self.scale = scale

    def __repr__(self):
        return '[%s %s %s %s] %s' % (
        self.x, self.y, self.z, self.translate, self.scale)

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

    def sensible_axes(self):
        """Returns a sensible uaxis and vaxis for this plane."""
        # TODO: Rewrite this method to allow non-90deg planes to work
        # Figure out which axes the plane exists in
        axes = [1, 1, 1]
        if self.v0.x == self.v1.x == self.v2.x:
            axes[0] = 0
        if self.v0.y == self.v1.y == self.v2.y:
            axes[1] = 0
        if self.v0.z == self.v1.z == self.v2.z:
            axes[2] = 0

        # Figure out uaxis xyz
        u = [0, 0, 0]
        for i in range(3):
            if axes[i] == 1:
                u[i] = 1
                axes[i] = 0
                break

        # Figure out vaxis xyz
        v = [0, 0, 0]
        for i in range(3):
            if axes[i] == 1:
                v[i] = -1
                break

        uaxis = Axis(u[0], u[1], u[2])
        vaxis = Axis(v[0], v[1], v[2])
        return (uaxis, vaxis)

class Output:

    """An output connection for an Entity. Used within 'connections' classes.

    Example:

    >>> conn = vmf.Connections()
    >>> conn.children.append(Output("OnTrigger", "bob", "ToggleSprite", "",
    ...     3.14, -1)
    >>> my_entity.children.append(conn)

    """

    def __init__(self, event, target, input, parameter='', delay=0, 
        times_to_fire=-1):
        self.event = event
        self.target = target
        self.input = input
        self.parameter = parameter
        self.delay = delay
        self.times_to_fire = times_to_fire

    def __repr__(self):
        return '"%s" "%s,%s,%s,%s,%s"' % (self.event, self.target, self.input,
            self.parameter, self.delay, self.times_to_fire)
