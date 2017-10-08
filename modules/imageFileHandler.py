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
def file_create(data):
    directory_create()
    filename = directory+"image"+str(count)+".jpg"
    image_file_created = open(filename, 'wb')
    image_file_created.write(data)
    image_file_created.close()

# Magic Numbers for Images
#img_data = {"jpg": {"start":"ffd8ff","end":"ffd9"}}
img_data = {"jpg": {"start": "ff d8 ff e0", "mid": "4a 46 49 46", "end": "ff d9"}}   # JFIF

# Extract Image Files
def file_extraction(data):
    time_now = datetime.datetime.now()
    print "Time now is %s" % (str(time_now))
    for key,value in img_data.iteritems():
        print "Searching for %s files..." % (key)
        list_data = re.findall('..',data.encode('hex'))
        list_data = " ".join(list_data)
        #print list_data
        #print data.encode('hex')
        regex_string = r"("+re.escape(value["start"])+r".+?"+re.escape(value["end"])+r")"
        #regex_string = r"(" + re.escape(value["start"]) + r".+?" + re.escape(value["mid"]) + r".+?" + re.escape(value["end"]) + r")"
        #regex_string = r"(" + re.escape(value["start"]) + r".+?" + r"!" + re.escape(value["start"]) + r".+?" + re.escape(value["end"]) + r")"
        #regex_string = r"(" + re.escape(value["start"]) + r".+?" + r"!" + re.escape(value["start"]) + r".+?" + re.escape(value["end"]) + r".+?" +re.escape(value["end"]) + r")"
        #regex_string = "(ffd8ff.+?!ffd8ff.+?ffd9)"
       ## jpegs_snatched = re.findall(regex_string, data.strip().encode('hex'))
        jpegs_snatched = re.findall(regex_string, list_data)
        regex_time = datetime.datetime.now()
        print "Regex time is %s" % (str(regex_time))
        if jpegs_snatched:
            for snatches in jpegs_snatched:
                check = re.search(r"("+re.escape(value["start"])+r".+?"+re.escape(value["start"])+r")",snatches)
                if not check:
                    ##print snatches
                    #print "\n"*10
                    global count
                    count = count + 1
                    #snatches =
                    try:
                     #snatches.replace(" ","")
                     snatches = ''.join(snatches.split())
                     #print "\n"*10
                     #print snatches
                     file_create(snatches.decode('hex'))
                    except:
                      #print "\n" * 10
                      #regex_string = r"(" + re.escape(value["start"]) + r".+?" + re.escape(value["end"]) + r".+?" + re.escape(value["end"]) + r")"
                      #file_create(.decode('hex'))
                      #print snatches
                      pass
        time_now = datetime.datetime.now()
        print "Time at end is %s" % (str(time_now))


        """
        for snatches in jpegs_snatched:
            print snatches
            global count
            count = count + 1
            break
            #file_create(snatches)
        """







