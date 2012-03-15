#===============================================================================
# FIle upload library - Handle file uploads
# 
# In this module, we will abstract some patterns that has to do with saving files.
# /steven 8th sep 2011. 
#===============================================================================

import os
import base64
from ctrleff import get_app
from util import random_string
import S3
import Image
import ExifTags
from local_config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,\
    S3_LOCATION, S3_BUCKET_NAME, S3_KEY_NAME
from S3 import S3Object
import time

MOBILE_OPTIMIZED_WIDTH = 480
MOBILE_OPTIMIZED_FILENAME_APPEND = "_optimized"
app = get_app()

def resize_img(img_path, basewidth=MOBILE_OPTIMIZED_WIDTH):
    img = Image.open(img_path)
    
    #rotate of exif info exists
    if not img._getexif() is None:
        found_exif = False
        for orientation in ExifTags.TAGS.keys() : 
            if ExifTags.TAGS[orientation]=='Orientation' :
                found_exif = True
                break
        exif=dict(img._getexif().items())
        
        if orientation in exif and found_exif:
            if exif[orientation] == 3: 
                img = img.rotate(180, expand=True)
            elif exif[orientation] == 6 : 
                img = img.rotate(270, expand=True)
            elif exif[orientation] == 8 : 
                img = img.rotate(90, expand=True)
    
    #resize image
    w, h = img.size
    wsize = basewidth 
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    if w > h:
        hsize = basewidth
        hpercent = (basewidth/float(img.size[1]))
        wsize = int((float(img.size[0])*float(hpercent)))
    img = img.resize((wsize,hsize), Image.ANTIALIAS)
    
    filename = os.path.basename(os.path.splitext(img_path)[0])
    parent = os.path.dirname(img_path)
    img.save(os.path.join(parent, filename+MOBILE_OPTIMIZED_FILENAME_APPEND+".jpg"), "JPEG")
    return os.path.join(parent, filename+MOBILE_OPTIMIZED_FILENAME_APPEND+".jpg")

def save_to_s3(unique_identifier, post_file, tmp_folder, encoded=None):
    """
    Saves file to Amazon S3 with a unique identifier. (Can be a user id)
    """
    conn = S3.AWSAuthConnection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    generator = S3.QueryStringAuthGenerator(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    key = S3_KEY_NAME + "_" + str(unique_identifier) + "_" + random_string() + "_" + str(int(time.time()))
    
    #check if bucket exists, if not cr8 it
    if not conn.check_bucket_exists(S3_BUCKET_NAME).status == 200:
        conn.create_located_bucket(S3_BUCKET_NAME, S3_LOCATION)
    
    #resize file
    absolute_write_path, file_name = temp_save_file(post_file, ".jpg", encoded, tmp_folder)
    resize_img(absolute_write_path)
    
    #upload orig file
    orig_file = open(absolute_write_path, "r")
    obj = S3Object(orig_file.read())
    conn.put(S3_BUCKET_NAME, key + ".jpg", obj)
    
    #upload resized file
    resized_filename = os.path.splitext(file_name)[0] + "_optimized.jpg"
    resized_file = open(os.path.join(tmp_folder, resized_filename),"r")
    obj = S3Object(resized_file.read())
    conn.put(S3_BUCKET_NAME, key+"_optimized.jpg", obj)
    
    #remove temp files
    os.remove(absolute_write_path)
    os.remove(os.path.join(tmp_folder, resized_filename))
    
    return key

def get_data_from_post_file(post_file, encoded=None):
    if encoded == None:
        encoded=True
        
    file_data = None
    if encoded:
        file_data = base64.b64decode(post_file)
    else: file_data = post_file.read()
    
    return file_data


def temp_save_file(post_file, extension, encoded, working_dir):
    file_data = get_data_from_post_file(post_file, encoded)
    file_name = random_string() + extension
    absolute_write_path = os.path.join(working_dir, file_name)
    while os.path.exists(absolute_write_path):
        file_name = random_string() + extension
        absolute_write_path = os.path.join(working_dir, file_name)
    
    file = open(absolute_write_path, 'wb+')
    file.write(file_data)
    file.close()
    return absolute_write_path, file_name

def save_file(post_file, extension=None, subdir=None, dir_to_save=None, encoded=None):
    """
    Saves a file to a directory.
    * file must be base64 encoded stream.
    - Ensures no file clashes.
    - Returns the filename.
    """
    
    if extension == None:
        extension = ".jpg"
    if dir_to_save == None:
        dir_to_save = app.config["upload_dir"]
    if subdir == None: 
        subdir = ""
    if encoded == None:
        encoded=True
        
    #ensure directory is created
    working_dir = os.path.join(dir_to_save, subdir)
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)
    
    absolute_write_path, file_name = temp_save_file(post_file, extension, encoded, working_dir)
    
    resize_img(absolute_write_path)
    
    return file_name

def open_file(file_name):
    """
    opens file in samples, and return base64 encoded streams.
    """
    sample_dir = app.config["samples_dir"]
    file = open(os.path.join(sample_dir, file_name), 'r')
    stream = file.read()
    encoded_stream = base64.b64encode(stream)
    return encoded_stream