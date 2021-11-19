# Notes

## **Objects**
The _Object Database_ stores and retrieves arbitrary blobs which are called "objects".  
The Object Database does not care about the internal structure of the a file.

The object is a low-level building block for working in Git. The object is referred to by it's hash.


The object are split into several directories to avoid directories with many files in order to improve performance.  
_note:_ This project will skip this step for sake of simplicity.

### **Command Details**
Commands needs to occur in the `.git` directory.

### **Hash Object**

```
> gitdown hash-object <objectname>
hash_of_object_contents
```

The `hash_object` takes a hash of the file.  
The flow of the `hash_object` command is:
* Get the path file of the store
* Read the file
* Hash the content of the file using SHA-1
* Store the file under `.gitdown/objects/(_SHA-1 hash of object_)`

This type of storage is called **content addressable** because the address used to find the blob is based on the contents of the blob itself.  
When Git stores objects it performs several other operations such as:
* writing the size of the object
* compressing objects and dividing them into 256 directories

### **Cat files**
```
> gitdown cat-file <hash_of_object_contents>
objectname
```
The `cat-file` command does the opposite of `hash-object`. It prints the object by its OID.  
It reads the content of `.gitdown/objects/{OID}`.

### **Types of Objects**
Objects are assigned a "type". The type is a string that is prepended to the start of the file, followed by a null byte.  
There are different types of that are used in diffent contexts.  
Different type tags will be added to ensure objects are used in the right context.  
When reading the file, the type will be used to verify that it is the intended type.

The default type is `blob`.

### **Base Module**
The base module will have the basic higher-level logic of git. 
For example, it will use the object database to implement higher-level structures for storing directories.


### **write-tree**
The `write-tree` command stores the current working directory in the object database.  
`hash-object` stores a file and `write-tree` stores a whole directory.
Both operations return an OID.

In Git a "tree" refers to a directory.

`write-tree` will be written in the _base module_ because it doesn't write directly o disk but uses the  
object database from _data_ to store the directory.