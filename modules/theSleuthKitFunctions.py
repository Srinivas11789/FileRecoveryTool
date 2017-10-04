# Sleuth Kit Python Binding Library
import pytsk3
# Extensive Witness Format - Extension to Python 
#import pyewf

# Disk Image File Open
def diskImageFileOpen(image_file):
    tsk_image_file_handle = pytsk3.tsk_img_open(image_file)
    return tsk_file_handle

# Disk Image File Information
def diskImageFileInfo(image_file):
    return pytsk3.Img_Info(image_file)

# Disk Image Volume Information
def diskImageVolumeInfo(image_file):
    return pytsk3.Volume_Info(image_file)







     
