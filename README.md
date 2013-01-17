vmflib: a Python module for creating Valve Map Format (VMF) files
=================================================================

vmflib is a python module to help developers create maps for 
VMF-compatible video games procedurally using Python. The VMF format
is best known for its use in the Source Engine and its many games.


Current Status
--------------

This is a new project, and is very far from completion.

In the meantime, if there's something you wish to contribute,
message me or send me a pull request. Contributions are welcome.


Usage
-----

Current functionality is very limited (to say the least), but
the general usage is as follows:

```python
import vmf

m = vmf.ValveMap()

# do stuff with m

m.write_vmf("mymap.vmf")
```


License
-------

vmflib is provided freely under the Simplified BSD License.
See LICENSE for full details.
