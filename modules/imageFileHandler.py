########################################################################################################
#
#                     Image File Extractor Module - Handles JPEG PNG from a given Data
#
#########################################################################################################

import os, re

# Global Variable COUNT - to keep track of files as they are found
main_path = os.getcwd()
count = 0
directory = "report/jpg/"

# Folder Creator For Jpeg Files
def directory_create():
 if not os.path.exists(directory):
    os.makedirs(directory)

# Create Image Files with the Data Given
def file_create(data):
    directory_create()
    filename = directory+"image"+str(count)+".jpg"
    image_file_created = open(filename, 'wb')
    image_file_created.write(data)
    image_file_created.close()

# Magic Numbers for Images
img_data = {"jpg":{"start":"ffd8","end":"ffd9"},}

# Extract Image Files
def file_extraction(data):
    for type in img_data:
        print "Searching for %s files..." % (type)
        #print data.encode('hex')
        jpegs_snatched = re.findall("(ffd8(.+?)ffd9)", data.encode('hex').strip())
        if jpegs_snatched:
            for snatches in jpegs_snatched:
                #print snatches[0]
                #print "\n"*10
                global count
                count = count + 1
                try:
                 file_create(snatches[0].strip().decode('hex'))
                except:
                  pass


        """
        for snatches in jpegs_snatched:
            print snatches
            global count
            count = count + 1
            break
            #file_create(snatches)
        """







