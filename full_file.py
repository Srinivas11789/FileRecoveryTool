##########################################################################################################################
#
#
#                                 File Recovery Script - A File Recovery Program
#
#                                   Author: Srinivas Piskala Ganesh Babu
#
#
#
############################################################################################################################

# Module Import
import sys
import sqlite3
from prettytable import PrettyTable
import json
import os
import re
import datetime
import hashlib
import warnings

try:
    import pyPdf
    pdfinfo_compatibility = "True"
except:
    pdfinfo_compatibility = "False"

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    from PIL import Image
    from PIL.ExifTags import TAGS

    exifinfo_compatibility = "True"
except:
    exifinfo_compatibility = "False"


main_path = os.getcwd()

# Path Setting
sys.path.insert(0, 'modules/')


########################################################################################################
#
#                     Image File Extractor Module - Handles JPEG PNG from a given Data
#
#########################################################################################################

# Global Variable COUNT - to keep track of files as they are found
image_count = 0

# Folder Creator For Jpeg Files
def image_directory_create(type):
    directory = r"report/" + type + r"/"
    if not os.path.exists(directory):
        os.makedirs(directory)

# Create Image Files with the Data Given
def image_file_create(data, type):
    image_directory_create(type)
    filename = r"report/" + type + r"/" + "image" + str(image_count) + "." + type
    image_file_created = open(filename, 'wb')
    image_file_created.write(data)
    image_file_created.close()

# Magic Numbers for Images
img_data = {"jpg": {"start": "ffd8ffe0", "end": "ffd9"}, "bmp": {"start": "424d"},
            "png": {"start": "89504e47"}}  # JFIF

# Extract Image Files
def image_file_extraction(data):
    for key, value in img_data.iteritems():
        print "Searching for %s files..." % (key)
        if key == "jpg":
            regex_string = r"(" + re.escape(value["start"]) + r".+?" + re.escape(value["end"]) + r")"
            jpegs_snatched = re.findall(regex_string, data.strip().encode('hex'))
            if jpegs_snatched:
                for snatches in jpegs_snatched:
                    check = re.search(r"(" + re.escape(value["start"]) + r".+?" + re.escape(value["start"]) + r")",
                                      snatches)
                    if not check:
                        global image_count
                        image_count = image_count + 1
                        try:
                            snatches = ''.join(snatches.split())
                            image_file_create(snatches.decode('hex'), key)
                        except Exception, e:
                            if "Odd" in str(e):
                                while len(snatches) % 2 != 0:
                                    regex_string = r"(" + re.escape(snatches) + r".+?" + re.escape(
                                        value["end"]) + r")"
                                    fetch = re.search(regex_string, data.encode('hex'))
                                    snatches = fetch.group(1)
                                image_file_create(fetch.group(1).decode('hex'), key)
                            pass
            elif key == "bmp":
                check = re.search(re.escape(value["start"]), data.encode('hex'))
                if check:
                    print "BMP Signatures Found... Logic for Fetching length of BMP files 4 bytes from Header to be added!"
            elif key == "png":
                check = re.search(re.escape(value["start"]), data.encode('hex'))
                if check:
                    print "PNG Signatures Found... Logic for Fetching length of PNG files to be added!"

# File Metadata Extraction
def image_file_metadata_extract(file):
    metadata = {}
    if exifinfo_compatibility == "True":
        imagefile = Image.open(os.path.join(r"report/" + "jpg" + r"/", file))
        try:
            exifdata = imagefile._getexif()
        except Exception, e:
            pass
        if exifdata:
            for key, value in exifdata.items():
                metadata[TAGS.get(key, key)] = value
    else:
        print "PIL Module is not present - MetaData Extraction from image files failed!"
    return str(metadata)

# File MD5 Calculation
def image_file_md5_calculate(file):
    original_hash = hashlib.md5(open(r"report/" + "jpg" + r"/" + file, 'rb').read()).hexdigest()
    return str(original_hash)

########################################################################################################
#
#                     Ordinary File Extractor Module - Handles normal files
#
#########################################################################################################

def ordinary_file_open(list_of_files):

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


def ordinary_copy_memory(list_of_handles):

     # Read Memory
     read_of_files = []

     # Multiple Handles for Read
     for handle in list_of_handles:
         read = handle.read()
         read_of_files.append(read)

     return "".join(read_of_files)


########################################################################################################
#
#                     PDF File Extractor Module - Handles PDF from a given Data
#
#########################################################################################################



# Global Variable COUNT - to keep track of files as they are found
pdf_count = 0
pdf_directory = "report/pdf/"

# Folder Creator For Jpeg Files
def pdf_directory_create():
 if not os.path.exists(pdf_directory):
    os.makedirs(pdf_directory)

# Create Image Files with the Data Given
def pdf_file_create(data):
    pdf_directory_create()
    filename = pdf_directory+"pdf"+str(pdf_count)+".pdf"
    pdf_file_created = open(filename, 'wb')
    pdf_file_created.write(data)
    pdf_file_created.close()

# Magic Numbers for Images
pdf_data = {"pdf": {"start":"25504446","end":"25454f460d"}}

# Extract Image Files
def pdf_file_extraction(data):
    for key,value in pdf_data.iteritems():
        print "Searching for %s files..." % (key)
        regex_string = r"("+re.escape(value["start"])+r".+?"+re.escape(value["end"])+r".+?"+re.escape(value["end"])+r")"
        jpegs_snatched = re.findall(regex_string, data.encode('hex'))
        if jpegs_snatched:
            for snatches in jpegs_snatched:
                global pdf_count
                pdf_count = pdf_count + 1
                try:
                 pdf_file_create(snatches.decode('hex'))
                except:
                  pass

# Meta Data Extraction
def pdf_file_metadata_extract(file):
    metadata = {}
    if pdfinfo_compatibility == "True":
      try:
        pdffile = pyPdf.PdfFileReader(open(r"report/"+"pdf"+r"/"+file, 'rb')).getDocumentInfo()
        metadata.update(pdffile)
      except Exception,e:
            pass
    else:
        print "PyPDF Module is not present - MetaData Extraction from PDF files failed!"
    return str(metadata)

# File MD5 Calculation
def pdf_file_md5_calculate(file):
    original_hash = hashlib.md5(open(r"report/"+"pdf"+r"/"+file, 'rb').read()).hexdigest()
    return str(original_hash)

def main():
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
    file_contents = ordinary_copy_memory(ordinary_file_open(files))

    image_file_extraction(file_contents)
    pdf_file_extraction(file_contents)

    if os.path.exists("report/jpg"):
      for file in os.listdir("report/jpg"):
        cur.execute("INSERT INTO recoveredFiles VALUES (?, ?, ?)", (file, image_file_md5_calculate(file), image_file_metadata_extract(file)))

    if os.path.exists("report/pdf"):
      for file in os.listdir("report/pdf"):
        cur.execute("INSERT INTO recoveredFiles VALUES (?, ?, ?)",(file, pdf_file_md5_calculate(file), pdf_file_metadata_extract(file)))

    sqlhandle.commit()

    result_report = open(r"report/" + "report.txt", 'wb')
    for row in cur.execute("SELECT * FROM recoveredFiles"):
        table_of_content.add_row([row[0], row[1], json.dumps(row[2])])
        result_report.write("\n" * 3)
        result_report.write("\nFilename: %s" % (row[0]))
        result_report.write("\nMd5 Hash: %s" % (row[1]))
        if row[2] != "{}":
            result_report.write("\nMetadata: ")
            result_report.write("\n\t"+str(json.dumps(row[2], indent=4, sort_keys=True))+"\n")
        else:
            result_report.write("\nMetadata: %s" % (row[2]))
        result_report.write("\n" * 3)

    result_report.write(str(table_of_content))
    result_report.close()

    sqlhandle.close()

# Driver Program
if __name__ == "__main__":
    main()