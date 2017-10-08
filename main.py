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
import os
import sys

# Custom Module Import
sys.path.insert(0, 'modules/')
import ordinaryFileHandle
import imageFileHandler
import pdfFileHandler

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

for file in os.listdir("report/jpg"):
    print imageFileHandler.file_metadata_extract(file, "jpg")
    print "\n"*10

for file in os.listdir("report/pdf"):
    print pdfFileHandler.file_metadata_extract(file)
    print "\n" * 10

