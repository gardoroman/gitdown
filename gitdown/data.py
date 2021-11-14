import hashlib
import os

"""
Responsible for managing data in the `.gitdown` directory. 
This module will interact with the files on disk.
"""

def init():
    os.makedirs(get_git_dir())
    os.makedirs(get_object_path())

def hash_object(data, type_ = 'blob'):
    obj = type_.encode() + b'\x00' + data
    oid = hashlib.sha1(obj).hexdigest()
    path = get_object_path(oid)
    with open(path, 'wb') as out:
        out.write(obj)
    return oid

def get_object(oid, expected='blob'):
    path = get_object_path(oid)
    with open(path, 'rb') as f:
        obj = f.read()
    
    type_, _, content = obj.partition(b'\x00')
    type_ = type_.decode

    if expected is not None:
        assert type_ == expected, f'Expected{expected}, got {type_}'
    
    return content


# Helper functions for data.py
def get_object_path(oid = None):
    git_dir = get_git_dir()
    path = create_path(git_dir, 'objects')
    if oid:
        path = create_path(path, oid)

    return path

def get_git_dir():
    return '.gitdown'

def create_path(path, suffix):
    return os.path.join(path, suffix)