#! /usr/bin/env python3
"""

Utility for building a map using installed Source SDK tools.
Call with -h or --help to see usage information.

Examples:

  # Creates/installs/runs .bsp in same dir
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
import urllib.parse
import shutil

win32 = sys.platform.startswith('win32')
cygwin = sys.platform.startswith('cygwin')
linux = sys.platform.startswith('linux')
darwin = False  # Not supported yet

games = {
    'tf2': {
        'id': 440,
        'dir': os.path.join("Team Fortress 2", "tf"),
        'common': True  # Game lives under "common" rather than "<username>"
    },
    'css': {
        'id': 240,
        'dir': os.path.join("Counter-Strike Source", "cstrike"),
        'common': False
    },
    'hl2': {
        'id': 220,
        'dir': os.path.join("Half-Life 2", "hl2"),
        'common': False
    },
    'hl2mp': {
        'id': 320,
        'dir': os.path.join("Half-Life 2 Deathmatch", "hl2mp"),
        'common': False
    },
    'gm': {
        'id': 4000,
        'dir': os.path.join("GarrysMod", "garrysmod"),
        'common': False
    }
}

def get_game_dir(game, username=False):
    """Returns joined game directory path relative to Steamapps"""
    if not games[game]['common'] and not username:
        raise RuntimeError("Can't determine this game's directory without username")
    if games[game]['common']:
        subdir = "common"
    else:
        subdir = "username"
    subsubdir = games[game]['dir']
    if win32 or cygwin:
        subsubdir = subsubdir.lower()
    return os.path.join(subdir, subsubdir)

def _make_arg_parser():
    parser = argparse.ArgumentParser(description='Build, install, and test a VMF map.')
    parser.add_argument('map')
    parser.add_argument('-g', '--game', default='tf2', choices=games.keys(),
        help="selects which game to use")
    parser.add_argument('--no-run', action="store_true",
        help="don't run the game after building/installing")
    parser.add_argument('--no-install', action="store_true",
        help="don't install (or run) the map after building")
    parser.add_argument('-f', '--fast', action="store_true",
        help="enable fast compile options")
    parser.add_argument('--hdr', action="store_true",
        help="enable full HDR compile")
    parser.add_argument('--final', action="store_true",
        help="use with --hdr for slow high-quality HDR compile")
    parser.add_argument('--sourcesdk',
        help="location of your sourcesdk folder (for linux/wine)")

    return parser

def main():
    parser = _make_arg_parser()
    args = parser.parse_args()
    vmf_file = os.path.abspath(args.map)
    path, filename = os.path.split(vmf_file)
    mapname = filename[:-4]
    mappath = os.path.join(path, mapname)
    bsp_file = os.path.join(path, mapname + ".bsp")
    
    # Get sourcesdk path
    if win32 or cygwin:
        sourcesdk = os.environ['sourcesdk']
        if cygwin:
            def cygwin2dos(path):
                return subprocess.check_output(["cygpath", '-w', '%s' % path], universal_newlines=True).strip()
            sourcesdk = subprocess.check_output(["cygpath", sourcesdk], universal_newlines=True).strip()
        sourcesdk = os.path.abspath(sourcesdk)
    elif linux:
        sourcesdk = args.sourcesdk
        if not sourcesdk:
            sourcesdk = os.getenv('sourcesdk')
        if not sourcesdk:
            print("You need to pass the --sourcesdk argument or set the $sourcesdk env variable.")
            exit(-1)
        sourcesdk = os.path.abspath(sourcesdk)
    
    # Collect some other useful paths and info
    steamapps = os.path.dirname(os.path.dirname(sourcesdk)) # Full path to steamapps dir
    username = os.path.basename(os.path.dirname(sourcesdk))
    sdkbin = os.path.join(sourcesdk, "bin", "orangebox", "bin")
    game = games[args.game]
    gamedir = os.path.join(steamapps, get_game_dir(args.game, username))
    mapsdir = os.path.join(gamedir, "maps")

    # TF2 SteamPipe workaround
    if args.game == 'tf2':
        sdkbin = os.path.join(os.path.dirname(gamedir), "bin")
    
    # Make sure gamedir path seems legit
    if not os.path.isfile(os.path.join(gamedir, "gameinfo.txt")):
        raise Exception("Game directory does not contain a gameinfo.txt: %s" % gamedir)
    
    if win32 or cygwin:
        # Convert some paths if using Cygwin
        if cygwin:
            gamedir = cygwin2dos(gamedir)
            mappath = cygwin2dos(mappath)

        # Change working directory first because VBSP is dumb
        os.chdir(os.path.join(sourcesdk, 'bin', 'orangebox'))

        # Run the SDK tools
        vbsp_exe = os.path.join(sdkbin, "vbsp.exe")
        code = subprocess.call([vbsp_exe, '-game', gamedir, mappath])
        print("VBSP finished with status %s." % code)

        if code == 1:
            print("Looks like SteamService isn't working. Try reopening Steam.")
            exit(code)
        elif code == -11:
            print("Looks like you might have gotten the 'material not found' " +
                "error messages. Try signing into Steam, or restarting it " +
                "and signing in.")
            exit(code)
        elif code != 0:
            print("Looks like VBSP crashed, but I'm not sure why.")
            exit(code)

        vvis_exe = os.path.join(sdkbin, "vvis.exe")
        opts = [vvis_exe]
        if args.fast:
            opts.append('-fast')
        opts.extend(['-game', gamedir, mappath])
        subprocess.call(opts)

        vrad_exe = os.path.join(sdkbin, "vrad.exe")
        opts = [vrad_exe]
        if args.fast:
            opts.extend(['-bounce', '2', '-noextra'])
        if args.hdr:
            opts.append('-both')
        if args.hdr and args.final:
            opts.append('-final')
        opts.extend(['-game', gamedir, mappath])
        subprocess.call(opts)

        # Install the map to the game's map directory (unless --no-install)
        if not args.no_install:
            print("Copying map %s to %s" % (mapname, mapsdir))
            shutil.copy(bsp_file, mapsdir)
        else:
            print("Not installing map")

        # Launch the game (unless --no-run or --no-install)
        if not args.no_run and not args.no_install:
            params = urllib.parse.quote("-dev -console -allowdebug +map %s" % mapname)
            run_url = "steam://run/%d//%s" % (game['id'], params)
            print(run_url)
            webbrowser.open(run_url)
            if cygwin:
                print("\nYou're running cygwin, so I can't launch the game for you.")
                print("Double-click the URL above, right-click, and click 'Open'.")
                print("Or paste the URL above into the Windows 'Run...' dialog.")
                print("Or, just run 'map %s' in the in-game console." % mapname)
        else:
            print("Not launching game")
    elif linux:
        # Environment to use with wine calls
        env = os.environ.copy()
        env['WINEPREFIX'] = os.path.expanduser("~/.winesteam")
        
        # Define path-converting helper function
        def unix2wine(path):
            return subprocess.check_output(["winepath", '-w', '%s' % path], env=env).strip()
        
        # Wine-ify some of our paths
        gamedir = unix2wine(gamedir)
        mappath = unix2wine(mappath)

        # Tell wine to look for DLLs here
        #env['WINEDLLPATH'] = os.path.join(sourcesdk, "bin")
        
        #print("WINEDLLPATH is as follows: ", env['WINEDLLPATH'])

        # Use native maps directory instead of the Wine installation's
        mapsdir = os.path.join('~', '.steam', 'steam', 'SteamApps', get_game_dir(args.game, username), "maps")
        mapsdir = os.path.expanduser(mapsdir)

        # Change working directory first because VBSP is dumb
        os.chdir(os.path.join(sourcesdk, 'bin', 'orangebox'))
        
        print("Using -game dir: %s" % gamedir)
        
        # We now need to set the VPROJECT env variable
        env['VPROJECT'] = gamedir

        # Run the SDK tools
        vbsp_exe = os.path.join(sdkbin, "vbsp.exe")
        code = subprocess.call(['wine', vbsp_exe, '-game', gamedir, mappath], env=env)
        print("VBSP finished with status %s." % code)

        # Handle various exit status codes VBPS may have returned
        if code == 1:
            print("\nLooks like SteamService isn't working. Try reopening (wine's copy of) Steam:")
            steambin = os.path.join(os.path.dirname(steamapps), 'steam.exe')
            print('\nWINEPREFIX="%s" wine "%s" -no-dwrite' % (env['WINEPREFIX'], steambin))
            exit(code)
        elif code == -11:
            print("\nLooks like you might have gotten the 'material not found' " +
                "error messages. Try signing into Steam, or restarting it " +
                "and signing in.")
            exit(code)
        elif code != 0:
            print("\nLooks like VBSP crashed, but I'm not sure why.")
            exit(code)

        vvis_exe = os.path.join(sdkbin, "vvis.exe")
        opts = ['wine', vvis_exe]
        if args.fast:
            opts.append('-fast')
        opts.extend(['-game', gamedir, mappath])
        code = subprocess.call(opts, env=env)

        if code != 0:
            print("\nLooks like VVIS crashed, but I'm not sure why.")
            exit(code)

        vrad_exe = os.path.join(sdkbin, "vrad.exe")
        opts = ['wine', vrad_exe]
        if args.fast:
            opts.extend(['-bounce', '2', '-noextra'])
        if args.hdr:
            opts.append('-both')
        if args.hdr and args.final:
            opts.append('-final')
        opts.extend(['-game', gamedir, mappath])
        code = subprocess.call(opts, env=env)
        
        if code != 0:
            print("\nLooks like VRAD crashed, but I'm not sure why.")
            exit(code)

        # Install the map to the game's map directory (unless --no-install)
        if not args.no_install:
            shutil.copy(bsp_file, mapsdir)
        else:
            print("Not installing map")

        # Launch the game (unless --no-run or --no-install)
        if not args.no_run and not args.no_install:
            params = urllib.parse.quote("-dev -console -allowdebug +map %s" % mapname)
            run_url = "steam://run/%d//%s" % (game['id'], params)
            print(run_url)
            webbrowser.open(run_url)
        else:
            print("Not launching game")
    else:
        raise OSError('Your OS is not supported yet!')

if __name__ == '__main__':
    main()
