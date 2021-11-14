## Notes
The _Object Database_ stores and retrieves arbitrary blobs which are called "objects".  
The Object Database does not care about the internal structure of the a file.

The `hash_object` command needs to occur in the `.git` directory.

The object is a low-level building block for working in Git. The object is referred to by it's hash.

The flow of the `hash_object` command is:
* Get the path file of the store
* Read the file
* Hash the content of the file using SHA-1
* Store the file under `.gitdown/objects/(_SHA-1 hash of object_)`

This type of storage is called **content addressable** because the address used to find the blob is based on the contents of the blob itself.  
When Git stores objects it performs several other operations such as:
* writing the size of the object
* compressing objects and dividing them into 256 directories

The object are split into several directories to avoid directories with many files in order to improve performance.  
_note:_ This project will skip this step for sake of simplicity.

### **Refactor**
Change _f-string logic_ to us `os.join.path`

The `cat-file` command does the opposite of `hash-object`. It prints the object by its OID.  
It reads the content of `.gitdown/objects/{OID}`.




