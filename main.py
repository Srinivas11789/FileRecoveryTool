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
import sqlite3

# Custom Module Import
sys.path.insert(0, 'modules/')
import ordinaryFileHandle
import imageFileHandler
import pdfFileHandler

# Multiple Files Reception from the Arguments
if len(sys.argv) < 2:
   print "Enter the Image Filenames to Extract Images/PDF Files!\n"
   sys.exit()

# Argument Fetching
files = sys.argv[1:]

# Report Folder Creation (Future Get the Report as Argument)
directory = "report"
if not os.path.exists(directory):
    os.makedirs(directory)

# SQL Database and Table Creation for Data Insertion
sqlhandle = sqlite3.connect(directory+r"/"+r"extractedFiles.db")
cur = sqlhandle.cursor()
try:
 cur.execute("""CREATE TABLE recoveredFiles (Filename text, md5Hash text, MetaData text)""")
except:
  pass

# Copy Contents of all the Files 
file_contents = ordinaryFileHandle.copyMemory(ordinaryFileHandle.fileOpen(files))

imageFileHandler.file_extraction(file_contents)
pdfFileHandler.file_extraction(file_contents)

for file in os.listdir("report/jpg"):
  cur.execute("INSERT INTO recoveredFiles VALUES (?, ?, ?)", (file, imageFileHandler.file_md5_calculate(file), imageFileHandler.file_metadata_extract(file)))

for file in os.listdir("report/pdf"):
    cur.execute("INSERT INTO recoveredFiles VALUES (?, ?, ?)",(file, pdfFileHandler.file_md5_calculate(file), pdfFileHandler.file_metadata_extract(file)))

sqlhandle.commit()

#for row in cur.execute("SELECT * FROM recoveredFiles"):
#    print row

sqlhandle.close()