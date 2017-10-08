########################################################################################################
#
#                     Image File Extractor Module - Handles JPEG PNG from a given Data
#
#########################################################################################################

import os
import re
import datetime
import hashlib
try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    exifinfo_compatibility = "True"
except:
    exifinfo_compatibility = "False"

# Global Variable COUNT - to keep track of files as they are found
main_path = os.getcwd()
count = 0

# Folder Creator For Jpeg Files
def directory_create(type):
 directory = r"report/"+type+r"/"
 if not os.path.exists(directory):
    os.makedirs(directory)

# Create Image Files with the Data Given
def file_create(data, type):
    directory_create(type)
    filename = r"report/"+type+r"/"+"image"+str(count)+"."+type
    image_file_created = open(filename, 'wb')
    image_file_created.write(data)
    image_file_created.close()

# Magic Numbers for Images
img_data = {"jpg": {"start": "ffd8ffe0", "end": "ffd9"}, "bmp":{"start": "424d"},"png":{"start": "89504e47"}}  # JFIF

# Extract Image Files
def file_extraction(data):
    for key,value in img_data.iteritems():
        print "Searching for %s files..." % (key)
        if key == "jpg":
            regex_string = r"("+re.escape(value["start"])+r".+?"+re.escape(value["end"])+r")"
            jpegs_snatched = re.findall(regex_string, data.strip().encode('hex'))
            if jpegs_snatched:
                for snatches in jpegs_snatched:
                    check = re.search(r"("+re.escape(value["start"])+r".+?"+re.escape(value["start"])+r")",snatches)
                    if not check:
                        global count
                        count = count + 1
                        try:
                         snatches = ''.join(snatches.split())
                         file_create(snatches.decode('hex'), key)
                        except Exception, e:
                            if "Odd" in str(e):
                                while len(snatches) % 2 != 0:
                                    regex_string = r"("+re.escape(snatches)+r".+?"+re.escape(value["end"])+r")"
                                    fetch = re.search(regex_string, data.encode('hex'))
                                    snatches = fetch.group(1)
                                file_create(fetch.group(1).decode('hex'), key)
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
def file_metadata_extract(file, type):
    metadata = {}
    if exifinfo_compatibility == "True":
        imagefile = Image.open(os.path.join(r"report/"+type+r"/", file))
        try:
         for key, value in imagefile._getexif().items():
            metadata[TAGS.get(key, key)] = value
        except Exception,e:
            pass
    else:
        print "PIL Module is not present - MetaData Extraction from image files failed!"
    return metadata

# File MD5 Calculation
def file_md5_calculate(file):
    original_hash = hashlib.md5(open(file, 'rb').read()).hexdigest()
    return original_hash







