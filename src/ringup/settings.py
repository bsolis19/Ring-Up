from dotenv import load_dotenv
load_dotenv(verbose=True)

import os

APP_NAME=os.getenv('APP_NAME')
WINDOW_HEIGHT=os.getenv('WINDOW_HEIGHT')
WINDOW_WIDTH=os.getenv('WINDOW_WIDTH')

