########################################################################################################
#
#                     PDF File Extractor Module - Handles PDF from a given Data
#
#########################################################################################################

import os
import re
import hashlib
try:
    import pyPdf
    pdfinfo_compatibility = "True"
except:
    pdfinfo_compatibility = "False"

# Global Variable COUNT - to keep track of files as they are found
main_path = os.getcwd()
count = 0
directory = "report/pdf/"

# Folder Creator For Jpeg Files
def directory_create():
 if not os.path.exists(directory):
    os.makedirs(directory)

# Create Image Files with the Data Given
def file_create(data):
    directory_create()
    filename = directory+"pdf"+str(count)+".pdf"
    image_file_created = open(filename, 'wb')
    image_file_created.write(data)
    image_file_created.close()

# Magic Numbers for Images
img_data = {"pdf": {"start":"25504446","end":"25454f460d"}}

# Extract Image Files
def file_extraction(data):
    for key,value in img_data.iteritems():
        print "Searching for %s files..." % (key)
        regex_string = r"("+re.escape(value["start"])+r".+?"+re.escape(value["end"])+r".+?"+re.escape(value["end"])+r")"
        jpegs_snatched = re.findall(regex_string, data.encode('hex'))
        if jpegs_snatched:
            for snatches in jpegs_snatched:
                global count
                count = count + 1
                try:
                 file_create(snatches.decode('hex'))
                except:
                  pass

# Meta Data Extraction
def file_metadata_extract(file):
    metadata = {}
    if pdfinfo_compatibility == "True":
      try:
        pdffile = pyPdf.PdfFileReader(file(file, 'rb')).getDocumentInfo()
        metadata.update(pdffile)
      except Exception,e:
            pass
    else:
        print "PyPDF Module is not present - MetaData Extraction from PDF files failed!"
    return metadata

# File MD5 Calculation
def file_md5_calculate(file):
    original_hash = hashlib.md5(open(file, 'rb').read()).hexdigest()
    return original_hash






