import hashlib
import os

"""
Responsible for managing data in the `.gitdown` directory. 
This module will interact with the files on disk.
"""

GIT_DIR = '.gitdown'

def init():
    os.makedirs(GIT_DIR)
    os.makedirs(f'{GIT_DIR}/objects')

def hash_object(data):
    oid = hashlib.sha1(data).hexdigest()
    with open(f'{GIT_DIR}/objects/{oid}', 'wb') as out:
        return oid