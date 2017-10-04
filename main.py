# Module Import
import os, sys

# Custom Module Import
sys.path.insert(0, 'modules/')
import ordinaryFileHandle
import theSleuthKitFunctions 

# Multiple Files Reception from the Arguments
files = sys.argv[1:]


# Copy Contents of all the Files 
file_contents = ordinaryFileHandle.copyMemory(ordinaryFileHandle.fileOpen(files))

# Disk Image Information
print theSleuthKitFunctions.diskImageVolumeInfo(sys.argv[1])
print theSleuthKitFunctions.diskImageFileInfo(sys.argv[1])

