vmflib: a Python module for creating Valve Map Format (VMF) files
=================================================================

vmflib is a python module to help developers create maps for 
VMF-compatible video games procedurally using Python. The VMF format
is best known for its use in the Source Engine and its many games.


Current Status
--------------

This project is far from completion, but there's already a bit you can do
with it. See the **examples** directory for some easy-to-read demonstrations
of how vmflib can be used to produce some basic maps.

If there's something you wish to contribute, message me or send me a pull
request. Contributions are welcome. If you're doing something with vmflib or
using it in a project of your own, let me know -- I'd love to hear about it!


Usage
-----

Current functionality is pretty basic, but it's enough to get you by.
This is the basic workflow:

```python
import vmf

m = vmf.ValveMap()

# do stuff with m

m.write_vmf("mymap.vmf")
```

You can modify world attributes such as the sky name:

```python
m.world.skyname = 'sky_day01_01'
```

Or create a Block and add it to the world:

```python
from vmf.types import Vertex
from vmf.tools import Block

block = Block(Vertex(0, 0, -512), (1024, 1024, 64), 'BRICK/BRICKFLOOR001A')
m.world.children.append(block)
```

If you'd like to quickly start playing with vmflib interactively, simply
navigate to the folder where you cloned this repository and run `test.py`:

    $ ./test.py 

    You now have a clean ValveMap object to tinker with called "m".
    Try calling m.write_vmf("testmap.vmf") to output it as a VMF file.

    Or just type "m" to view the map's markup immediately.

    CTRL+D to exit.

    >>> 


Modules
-------

The functionality of this package is spread out across a handful of included
modules. Here is a run-down of the modules that exist so far and what they
do:

* vmf: Core classes used in defining maps, most notably the `ValveMap` class.
* types: Classes for representing some special data types that exist throughout
  the VMF specification (`Vertex`, `RGB`, `Bool`, and so on).
* brush: Classes used for modelling and representing basic geometry in the map
  (`Solid` and `Side`).
* tools: Classes that provide higher-level management of brush geometry (just
  `Block` for now) These abstractions don't exist within the VMF spec, so it is
  up to the tool (e.g. Hammer, or this library) to manage them internally.


License
-------

vmflib is provided freely under the Simplified BSD License.
See LICENSE for full details.
