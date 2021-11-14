import os

"""
Responsible for managing data in the `.gitdown` directory. 
This module will interact with the files on disk.
"""

GIT_DIR = '.gitdown'

def init():
    os.makedirs(GIT_DIR)