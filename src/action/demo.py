from os.path import join as j
import datetime

FOOD_NAME = "Succulent Sushi"
FOOD_DESC = """Mm. Thats a yummy picture of succulent sushi. But firstly, hello!\n"
Thank you for trying out the app.\n 
ctrlEFF allows you to capture experiences like this so you would never forget it.\n
All you have to do is capture Checkpoints as you discover great experiences, such as this great sushi meal.\n
Just whip out your phone, open the ctrlEFF app, and then capture a new Checkpoint by simply taking a picture and then entering some information about it. Thats it!\n
ctrlEFF will save the GPS location of the Checkpoint, and now you can easily revisit the place without fear of getting lost.\n
But we don't just do food, what about shopping? Tap the back button, and scroll right to see the demo shopping Checkpoint.  
"""
SHOP_NAME = "Shoes from Bugis Street Store"
SHOP_DESC = """Cheap shoes from Bugis Street, prices are guaranteed to be cheap, quality is however not ensured.\n
Shopping Checkpoints are a great way for you to share shopping deals, great purchases, and sales promotions with your friends!\n
Anytime your friends come by a location that you had saved a new Checkpoint, your Checkpoint would show up in "Checkpoints near you".\n
And you too would be able to discover great experiences, be it shopping, or Food Checkpoints that your friends had saved before.\n
But that is not all, check out the demo Play Checkpoint! 
"""
PLAY_NAME = "Nightlife in Singapore"
PLAY_DESC = """We have quite a few nightlife spots in Singapore, but how would you know which are the good ones?\n
Now you need not fret. Be it nightlife, or anything fun, Checkpoints are interactable! Like it by tapping on the Heart icon on the top right corner,\n
or make a comment to the creator of the Checkpoint if you need more detailed recommendations.\n
The best thing is, if you like Checkpoints that you discover as you move about in your daily life using ctrlEFF, you can simply add it to your own catalog!\n
And the Checkpoint will be saved in your catalog of "My Checkpoints".\n
So yes! The next time you are wondering what to do next? Consult ctrlEFF. Your friends will always give a better recommendation that any guidebook can!\n
Have fun!\n\n
PS: You can delete the Demo Checkpoints from the Menu options.
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