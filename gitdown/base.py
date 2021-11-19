import os

from . import data

def write_tree(directory='.'):
    with os.scandir(directory) as it:
        for entry in it:
            full = f'{directory}/{entry.name}'
            if is_ignored(full):
                print(f'true {full}')
                continue
            
            if entry.is_file(follow_symlinks=False):
                #Todo write the file to object store
                with open(full, 'rb') as f:
                    print(data.hash_object(f.read()), full)
            elif entry.is_dir(follow_symlinks=False):
                write_tree(full)

    #todo create the trea object

def is_ignored(path):
    return '.gitdown' in path.split('/') or '.git' in path.split('/')
