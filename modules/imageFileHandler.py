########################################################################################################
#
#                     Image File Extractor Module - Handles JPEG PNG from a given Data
#
#########################################################################################################

import os, re, datetime

# Global Variable COUNT - to keep track of files as they are found
main_path = os.getcwd()
count = 0
directory = "report/jpg/"

# Folder Creator For Jpeg Files
def directory_create():
 if not os.path.exists(directory):
    os.makedirs(directory)

# Create Image Files with the Data Given
def file_create(data, type):
    directory_create()
    filename = directory+"image"+str(count)+"."+type
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






