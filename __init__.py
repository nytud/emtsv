import sys
import os

sys.path.append(os.path.dirname(__file__))

from xtsv.pipeline import init_everything, build_pipeline
from xtsv.tsvhandler import process
from config import tools, presets
