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
    'tf2': '',
    'css': '',
    'hl2': ''
    }

def _make_arg_parser():
    parser = argparse.ArgumentParser(description='Build a VMF map.')
    parser.add_argument('map')
    parser.add_argument('-g', '--game', default='tf2', choices=games.keys())
    parser.add_argument('--no-run')
    parser.add_argument('--no-install')

    return parser

if __name__ == '__main__':
    parser = _make_arg_parser()
    args = parser.parse_args()
    #opts, args = arg_parser.parse_args()
    
    if sys.platform.startswith('win32'):
        # TODO:
        # - Figure out paths we'll need (maybe detect where steam lives?)
        # - Use subprocess to call the tools
        print("I don't work yet!")
    else:
        raise OSError('Your OS is not supported yet!')
