import sys
import os

if hasattr(sys, '_MEIPASS'):
    os.environ['MEDIAPIPE_DISABLE_GPU'] = '1'
    sys.path.insert(0, sys._MEIPASS)
