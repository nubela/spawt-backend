#===============================================================================
# util lib for serving static/media 
#===============================================================================
import os
from local_config import BASE_URL

def get_checkpoint_img_url(cp_obj):
    filename = os.path.splitext(cp_obj.image)[0]
    img_filename = filename + "_optimized.jpg"
    url_nodes = [BASE_URL, "static/uploads", str(cp_obj.creator), img_filename]
    return "/".join(url_nodes)