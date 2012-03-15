from os.path import join as j
import datetime

FOOD_NAME = "Succulent Sushi"
FOOD_DESC = """  
"""
SHOP_NAME = "Shoes from Bugis Street Store"
SHOP_DESC = """
"""
PLAY_NAME = "Nightlife in Singapore"
PLAY_DESC = """
"""

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
    return _add_cp(user_obj, FOOD_NAME, FOOD_DESC, food_img_path, type, "food.jpg", price=price)

def add_shop_cp(user_obj):
    from ctrleff import get_resources_abs_path
    shop_img_path = j(get_resources_abs_path(), "demo", "shop.jpg")
    expiry = datetime.datetime.now()
    type = "shop"
    return _add_cp(user_obj, SHOP_NAME, SHOP_DESC, shop_img_path, type, "shop.jpg", expiry=expiry)

def add_play_cp(user_obj):
    from ctrleff import get_resources_abs_path
    play_img_path = j(get_resources_abs_path(), "demo", "play.jpg")
    expiry = datetime.datetime.now()
    price = 10
    type = "play"
    return _add_cp(user_obj, PLAY_NAME, PLAY_DESC, play_img_path, type, "play.jpg", price=price)

def _add_cp(user_obj, name, desc, img_path, type, img_file_name, price=None, expiry=None):
    from util.fileupload import save_to_s3
    from ctrleff import get_resources_abs_path
    from action.checkpoint import add_checkpoint
    
    creator_id = user_obj.id
    longitude, latitude = 103.8, 1.3667
    
    checkpoint = add_checkpoint(creator_id, name, type, img_file_name, longitude, latitude, desc, price=price, expiry=expiry, demo=True, img_location="s3")
    return checkpoint