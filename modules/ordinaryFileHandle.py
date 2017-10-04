import os, sys

def fileOpen(list_of_files):

    # Multiple Files Reception - Explicit check and conversion to a list
    if not isinstance(list_of_files, list):
       list_of_files = list(list_of_files)

    # File Handlers
    list_of_handles = []

    # Create File Handles 
    for file in list_of_files:
        handle = open(file, 'rb')
        list_of_handles.append(handle)

    return list_of_handles


def copyMemory(list_of_handles):

     # Read Memory
     read_of_files = []

     # Multiple Handles for Read
     for handle in list_of_handles:
         read = handle.read()
         read_of_files.append(read)

     return "".join(read_of_files)


            

     

