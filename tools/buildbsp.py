#!/usr/bin/python3
"""

Utility for building a map using installed Source SDK tools.

Finished use should resemble something like:

  # Creates/installs/runs standard .bsp in same dir
  python buildbsp.py --game tf2 mymap.vmf
  
  # Creates/installs .bsp but does not run
  python buildbsp.py --game css --no-run mymap.vmf
  
  # Only create .bsp, and use fast config
  python buildbsp.py --game tf2 --no-run --no-install --fast mymap.vmf

"""

import argparse
import sys
import subprocess

games = {
    'tf2': {'id': 440},
    'css': {'id': 240},
    'hl2': {'id': 220},
    'gm': {'id': 4000}
    }

def _make_arg_parser():
    parser = argparse.ArgumentParser(description='Build a VMF map.')
    parser.add_argument('map')
    parser.add_argument('-g', '--game', default='tf2', choices=games.keys(),
        help="selects which game to use")
    parser.add_argument('--no-run',
        help="don't run the game after building/installing")
    parser.add_argument('--no-install',
        help="don't install (or run) the map after building")

    return parser

if __name__ == '__main__':
    parser = _make_arg_parser()
    args = parser.parse_args()
    #opts, args = arg_parser.parse_args()
    
    if sys.platform.startswith('win32'):
        # Environmental scan
        # - Figure out paths we'll need (maybe detect where steam lives?)
        # TODO
        
        # Run the SDK tools
        # - Use subprocess to call the tools
        # TODO
        
        # Install the map to the game's map directory (unless --no-install)
        # TODO
        
        # Launch the game (unless --no-run or --no-install)
        # TODO
        # steam://run/{id} -dev -console -allowdebug +map {mapname}
        print("I don't work yet!")        
    else:
        raise OSError('Your OS is not supported yet!')
