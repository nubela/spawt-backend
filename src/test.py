from facebook.facebook import get_app_access_code, create_test_user,\
    delete_all_test_users, make_friend_connection

app_xs_token = "167694509990429|sw3Tff95bdC--TCp-i0_0ffbB1A"
app_id = "167694509990429"

delete_all_test_users(app_id, app_xs_token)

user_a = create_test_user(app_id, app_xs_token)
user_b = create_test_user(app_id, app_xs_token)

print user_a
print user_b

make_friend_connection(user_a["id"], user_b["id"], user_a["access_token"], user_b["access_token"])