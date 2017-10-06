##########################################################################################################################
#
#
#                                   Main Function File - The Tool Driver Program
#
#                                   Author: Srinivas Piskala Ganesh Babu
#
#
#
############################################################################################################################

# Module Import
import os, sys

# Custom Module Import
sys.path.insert(0, 'modules/')
import ordinaryFileHandle
import imageFileHandler
import pdfFileHandler
#import theSleuthKitFunctions 

# Multiple Files Reception from the Arguments
if len(sys.argv) < 2:
   print "Enter the Image Filenames to Extract Images/PDF Files!\n"
   sys.exit()

files = sys.argv[1:]

# Report Folder Creation (Future Get the Report as Argument)
directory = "/Report"
if not os.path.exists(directory):
    os.makedirs(directory)

# Copy Contents of all the Files 
file_contents = ordinaryFileHandle.copyMemory(ordinaryFileHandle.fileOpen(files))

imageFileHandler.file_extraction(file_contents)
pdfFileHandler.file_extraction(file_contents)

"""
# Create a Temporary Memory to Analyze Combining all the Memory Files provided
temp_filename = "tempDisk.image"
temp_file = open(temp_filename,'wb')
temp_file.write(file_contents.encode('hex'))
temp_file.close()

# Temporary File - Handler as a Single File
temp_file = open(temp_filename,'rb')
print temp_file.readline()
"""

"""
# Disk Image Information
partition_info = theSleuthKitFunctions.diskImageVolumeInfo(theSleuthKitFunctions.diskImageFileInfo(temp_filename))

print partition_info
"""
