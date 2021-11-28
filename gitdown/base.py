import os

from . import data

#----------------------------------------------------------------------------
# `write_tree`
# takes the current working directory and stores it in the object database.
#----------------------------------------------------------------------------
def write_tree(directory='.'):
    entries = []
    with os.scandir(directory) as it:
        for entry in it:
            full = f'{directory}/{entry.name}'
            if is_ignored(full):
                continue
            
            if entry.is_file(follow_symlinks=False):
                type_ = 'blob'
                with open(full, 'rb') as f:
                    oid = data.hash_object(f.read())
            elif entry.is_dir(follow_symlinks=False):
                type_ = 'tree'
                oid = write_tree(full)

            entries.append((entry.name, oid, type_))

    tree = ''.join(f'{type_} {oid} {name}\n'
                    for name, oid, type_ in sorted(entries))

    return data.hash_object(tree.encode(), 'tree')

#----------------------------------------------------------------------------
# `_iter_tree_entries`
# is a generator that will take the OID of a tree,
# tokenize it line by line and yield the raw string value
#----------------------------------------------------------------------------
def _iter_tree_entries(oid):
    if not oid:
        return
    
    tree = data.get_object(oid, 'tree')
    for entry in tree.decode().splitlines():
        type_, oid, name = entry.split(' ', 2)
        yield type_, oid, name

#----------------------------------------------------------------------------
# `get_tree`
# uses` _iter_tree_entries` to recursively parse a tree into a dictionary
#----------------------------------------------------------------------------
def get_tree(oid, base_path=''):
    result = {}
    for type_, oid, name in _iter_tree_entries(oid):
        assert '/' not in name
        assert name not in ('..', '.')
        path = base_path + name
        if type_ == 'blob':
            result[path] = oid
        elif type == 'tree':
            result.update(get_tree(oid, f'{path}/'))
        else:
            assert False, f'Unkown tree entry {type_}'
    
    return result

#----------------------------------------------------------------------------
# `_empty_current_directory`
# delete any files left over after calling read-tree
#----------------------------------------------------------------------------
def _empty_current_directory():
    for root, dirnames, filenames in os.walk('.', topdown=False):
        for filename in filenames:
            path = os.path.relpath(f'{root}/{filename}')
            if is_ignored(path) or not os.path.isfile(path):
                continue
            os.remove(path)
        for dirname in dirnames:
            path = os.path.relpath(f'{root}/{dirname}')
            if is_ignored(path):
                continue
            try:
                os.rmdir(path)
            except(FileNotFoundError, OSError):
                # deletion might fail if the dir has ignored files
                pass

#----------------------------------------------------------------------------
# `read_tree`
# uses `get_tree` to get the file OIDs and writes them to the 
# working directory
#----------------------------------------------------------------------------
def read_tree(tree_oid):
    _empty_current_directory()
    for path, oid in get_tree(tree_oid, base_path='./').items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(data.get_object(oid))

#----------------------------------------------------------------------------
# `commit`
# Adds a object in Object DB with a type of `commit`.
# This entails creating a snapshot of key/values and a commit message
#----------------------------------------------------------------------------
def commit(message):
    commit = f'tree {write_tree()}\n'

    head = data.get_head()
    if head:
        commit += f'parent {head}\n'

    commit += '\n'
    commit += f'{message}\n'

    oid = data.hash_object(commit.encode(), 'commit')

    data.set_head(oid)
    
    return oid

def is_ignored(path):
    return '.gitdown' in path.split('/') or '.git' in path.split('/')
