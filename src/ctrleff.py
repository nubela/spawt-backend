#===============================================================================
# backend for ctrleff
#===============================================================================
from flask import Flask
from local_config import API_TO_REGISTER 

#utils

def get_resources_abs_path():
    
    #some nice shortcuts
    from os.path import realpath, dirname as pparent, join as pjoin
    
    here = realpath(__file__)
    return pjoin(pparent(pparent(here)) , "resources")

def get_app(static=None):
    """
    factory for app
    """
    if static:
        return static
    
    app =  Flask(__name__)
    init_app(app)
    static = app
    return app

def init_db():
    """
    creates the tables from schema
    """
    from db import db
    db.create_all()

def init_app(app):
    """
    initializes the app on first run
    - registeres it with apis
    """
    for api_name in API_TO_REGISTER:
        __import__("api." + api_name)
        getattr(api, api_name)._register_api(app)

if __name__ == '__main__':
    app = get_app()
    app.debug = True
    app.run(host='0.0.0.0')