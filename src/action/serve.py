#===============================================================================
# util lib for serving static/media 
#===============================================================================
import os
from local_config import BASE_URL, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,\
    S3_BUCKET_NAME
from util import S3

def get_checkpoint_img_url(cp_obj):
    #return s3 url
    if cp_obj.img_location is "s3":
        generator = S3.QueryStringAuthGenerator(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        url = generator.get(S3_BUCKET_NAME, cp_obj.image)
        return url
    
    #return local hosted url
    filename = os.path.splitext(cp_obj.image)[0]
    img_filename = filename + "_optimized.jpg"
    url_nodes = [BASE_URL, "static/uploads", str(cp_obj.creator), img_filename]
    return "/".join(url_nodes)