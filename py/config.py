# config.py
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

class Config:
    def __init__(self):
        self.VERBOSE = False


    def set_verbose(self, verbose):
        self.VERBOSE = verbose

# Create a global configuration instance
config = Config()
