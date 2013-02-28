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
import os
import subprocess
import webbrowser

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
    parser.add_argument('--no-run', action="store_true",
        help="don't run the game after building/installing")
    parser.add_argument('--no-install', action="store_true",
        help="don't install (or run) the map after building")
    parser.add_argument('--steamapps',
        help="location of your user's steamapps subfolder")

    return parser

if __name__ == '__main__':
    parser = _make_arg_parser()
    args = parser.parse_args()
    vmf_file = os.path.abspath(args.map)
    
    if sys.platform.startswith('win32'):
        # Define constants
        games['tf2']['gamedir'] = 'team fortress 2\tf'

        # Environmental scan
        # - Figure out paths we'll need (maybe detect where steam lives?)
        # Best I can figure out for now is accepting a path as an argument
        steamapps = os.path.abspath(args.steamapps)
        sdkbin = "%s\sourcesdk\bin\orangebox\bin" % steamapps
        game = games[args.game]
        gamedir = "%s\%s" % (steamapps, game['gamedir'])
        # TODO
        
        # Run the SDK tools
        # - Use subprocess to call the tools
        # TODO
        vbsp_cmd = '"%s\vbsp.exe" -game "%s" "%s"' % (sdkbin, gamedir, vmf_file)
        print(vbsp_cmd)
        
        # Install the map to the game's map directory (unless --no-install)
        # TODO
        
        # Launch the game (unless --no-run or --no-install)
        if not args.no_run and not args.no_install:
            webbrowser.open("steam://run/%d//-dev -console -allowdebug +map %s" % (game['id'], "outdoor"))
        else:
            print("Not launching game")

        print("I don't work yet!")        
    else:
        raise OSError('Your OS is not supported yet!')
