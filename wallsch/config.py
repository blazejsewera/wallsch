'''
All the constants and general variables not changed during runtime.
'''
from pathlib import Path
from tzlocal import get_localzone


CONFIG_FILE = Path.home()/Path('.config/wallsch/config.json')
FILELIST_FILE = Path.home()/Path('.config/wallsch/filelist.json')

local_timezone = get_localzone()

VERBOSE = False
SIMPLE_SCRIPT = True
