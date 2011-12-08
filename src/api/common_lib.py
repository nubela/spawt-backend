from flask.helpers import jsonify

def authorization_fail():
    return jsonify({"error": "Authorization fail."}), 403