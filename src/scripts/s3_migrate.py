#===============================================================================
# migrates checkpoints that are stored locally to the cloud (s3)
#===============================================================================
from ctrleff import get_resources_abs_path
from util.fileupload import save_to_s3
import os

def migrate_s3():
    """
    Migrates existing Checkpoints that are stored locally to Amazon S3.
    """
    from db import db, Checkpoint
    local_checkpoints = Checkpoint.query.filter_by(img_location=None)
    
    for cp in local_checkpoints:
        
        #save to s3
        resources_dir = get_resources_abs_path()
        img_path = os.path.join(resources_dir,"uploads",str(cp.creator),cp.image)
        img_file = open(img_path, 'r') 
        img_name = save_to_s3(cp.creator, img_file.read(), resources_dir, False)
        
        img_path_optimized = os.path.join(resources_dir,"uploads",str(cp.creator),cp.image + "_optimized.jpg")
        img_file_optimized = open(img_path_optimized, 'r') 
        save_to_s3(cp.creator, img_file_optimized.read(), resources_dir, False)
        
        #update the checkpoint
        cp.img_location = "s3"
        cp.image = img_name    
        db.session.add(cp)
    
    db.session.commit()
    
if __name__ == "__main__":
    migrate_s3()