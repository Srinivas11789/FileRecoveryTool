import os, sys

import imageFileHandle

files = sys.argv[1:]

file_contents = imageFileHandle.copyMemory(imageFileHandle.fileOpen(files))

print file_contents
