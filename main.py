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
from prettytable import PrettyTable
import json

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

# Result Table Creation
table_of_content = PrettyTable(['FileName', 'md5Hash', 'Metadata'])

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

result_report = open(r"report/" + "report.txt", 'wb')
for row in cur.execute("SELECT * FROM recoveredFiles"):
    table_of_content.add_row([row[0], row[1], json.dumps(row[2])])
    result_report.write("\n" * 3)
    #esult_report.write("=" * 100)
    result_report.write("\nFilename: %s" % (row[0]))
    result_report.write("\nMd5 Hash: %s" % (row[1]))
    if row[2] != "{}":
        #ans = json.loads(str(row[2]).replace("\'","\""))
        result_report.write("\nMetadata: ")
        result_report.write("\n\t"+str(json.dumps(row[2], indent=4, sort_keys=True))+"\n")
    else:
        result_report.write("\nMetadata: %s" % (row[2]))
    #result_report.write("=" * 100)
    result_report.write("\n" * 3)

result_report.write(str(table_of_content))
result_report.close()

sqlhandle.close()



