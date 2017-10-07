########################################################################################################
#
#                     PDF File Extractor Module - Handles PDF from a given Data
#
#########################################################################################################

import os, re

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
        #print data.encode('hex')
        regex_string = r"("+re.escape(value["start"])+r".+?"+re.escape(value["end"])+r".+?"+re.escape(value["end"])+r")"
        jpegs_snatched = re.findall(regex_string, data.encode('hex'))
        if jpegs_snatched:
            for snatches in jpegs_snatched:
                #print "\n" * 10
                #print snatches
                #print "\n"*10
                global count
                count = count + 1
                try:
                 file_create(snatches.decode('hex'))
                except:
                  pass




