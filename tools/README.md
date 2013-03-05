# Tools for vmflib

## buildbsp.py

For more convenient compilation and testing of the maps you generate
using vmflib, a build tool named `buildbsp.py` has been included.

`buildbsp.py` works on Windows (either with Cygwin or a standard
command prompt environment) and in Linux.

In Windows, you must have an instance of Steam running (specifically,
an instance containing the Source SDK and whichever game you're 
compiling your map against).

In Linux, you must have access to a Windows instance of Steam (perhaps
on another partition if you dual-boot) which has Source SDK and your
target game installed. This cannot be autodetected in Linux, so you
must provide the path to the sourcesdk directory
(/path/to/windows/steam/steamapps/username/sourcesdk) via the 
`--sourcesdk` command line argument or an environment variable
named `sourcesdk`.  After the map compiles, the tool will install it
to your native Linux installation of the target game and launch it.

### Usage

    $ tools/buildbsp.py --help
    usage: buildbsp.py [-h] [-g {hl2mp,gm,hl2,css,tf2}] [--no-run] [--no-install]
                       [-f] [--hdr] [--final] [--sourcesdk SOURCESDK]
                       map

    Build, install, and test a VMF map.

    positional arguments:
      map

    optional arguments:
      -h, --help            show this help message and exit
      -g {hl2mp,gm,hl2,css,tf2}, --game {hl2mp,gm,hl2,css,tf2}
                            selects which game to use
      --no-run              don't run the game after building/installing
      --no-install          don't install (or run) the map after building
      -f, --fast            enable fast compile options
      --hdr                 enable full HDR compile
      --final               use with --hdr for slow high-quality HDR compile
      --sourcesdk SOURCESDK
                            location of your sourcesdk folder (for linux/wine)
