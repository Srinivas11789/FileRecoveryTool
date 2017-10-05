########################################################################################################
#
#                     Image File Extractor Module - Handles JPEG PNG from a given Data
#
#########################################################################################################

import os, re

# Global Variable COUNT - to keep track of files as they are found
count = 0

# Folder Creator For Jpeg Files
def directory_create():
 directory = "../report/jpg"
 if not os.path.exists(directory):
    os.makedirs(directory)

# Create Image Files with the Data Given
def file_create(data):
    directory_create()
    filename = "/report/jpg/image"+count+".jpg"
    image_file_created = open(filename, 'wb')
    image_file_created.write(data)
    image_file_created.close()

# Magic Numbers for Images
img_data = {"jpg":{"start":"FF D8","end":"FF D9"},}

# Extract Image Files
def file_extraction(data):
    for type in img_data:
        print "Searching for %s files..." % (type)
        print data.encode('hex')
        jpegs_snatched = re.findall("FF D8(.+?)FF D9", data.encode('hex'))
        for snatches in jpegs_snatched:
            file_create(snatches)









