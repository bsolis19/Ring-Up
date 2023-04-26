from dotenv import load_dotenv
from pathlib import Path
# Get the base directory
basepath = Path()
basedir = str(basepath.cwd())
# Load the environment variables
envars = basepath.cwd() / '.env'
load_dotenv(envars, verbose=True)

import os
import platform

APP_NAME=os.getenv('APP_NAME')
WINDOW_HEIGHT=os.getenv('WINDOW_HEIGHT')
WINDOW_WIDTH=os.getenv('WINDOW_WIDTH')
CONFIG_DIR=os.getenv('CONFIG_DIR')
SYSTEM=platform.system()
