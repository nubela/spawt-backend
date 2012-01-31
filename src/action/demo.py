from os.path import join as j
import datetime

FOOD_NAME = "food"
FOOD_DESC = "food desc"
SHOP_NAME = "shop"
SHOP_DESC = "shop desc"
PLAY_NAME = "play"
PLAY_DESC = "play desc"

def create_demo_checkpoints(user_obj):
    from action.user_checkpoint import add_checkpoint_to_user
    """
    creates the 3 demo checkpoints of different type: play, food, shop
    for a user
    """
    
    food_cp = add_food_cp(user_obj)
    food_ucp = add_checkpoint_to_user(user_obj, food_cp) 
    
    shop_cp = add_shop_cp(user_obj)
    shop_ucp = add_checkpoint_to_user(user_obj, shop_cp)
    
    play_cp = add_play_cp(user_obj)
    play_ucp = add_checkpoint_to_user(user_obj, play_cp)
    
def add_food_cp(user_obj):
    from ctrleff import get_resources_abs_path
    food_img_path = j(get_resources_abs_path(), "demo", "food.jpg")
    price = 2.5
    type = "food"
    return _add_cp(user_obj, FOOD_NAME, FOOD_DESC, food_img_path, type, price=price)

def add_shop_cp(user_obj):
    from ctrleff import get_resources_abs_path
    shop_img_path = j(get_resources_abs_path(), "demo", "shop.jpg")
    expiry = datetime.datetime.now()
    type = "shop"
    return _add_cp(user_obj, SHOP_NAME, SHOP_DESC, shop_img_path, type, expiry=expiry)

def add_play_cp(user_obj):
    from ctrleff import get_resources_abs_path
    play_img_path = j(get_resources_abs_path(), "demo", "play.jpg")
    expiry = datetime.datetime.now()
    price = 10
    type = "play"
    return _add_cp(user_obj, PLAY_NAME, PLAY_DESC, play_img_path, type, price=price)

def _add_cp(user_obj, name, desc, img_path, type, price=None, expiry=None):
    from util.fileupload import save_file
    from ctrleff import get_resources_abs_path
    from action.checkpoint import add_checkpoint
    
    upload_dir = j(get_resources_abs_path(), "uploads")
    
    creator_id = user_obj.id
    longitude, latitude = 103.8, 1.3667
    image = open(img_path, "r")
    img_file_name = save_file(image, ".jpg", str(creator_id), upload_dir, encoded=False)
    
    checkpoint = add_checkpoint(creator_id, name, type, img_file_name, longitude, latitude, desc, price=price, expiry=expiry, demo=True)
    return checkpoint