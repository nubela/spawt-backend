#===============================================================================
# restful client thin library around urrlib2
#===============================================================================
from urllib import urlencode
import httplib
from simplejson import loads
from urlparse import parse_qsl
from datetime import datetime

REQ_CACHE = {} 

DATEFORMAT = "%Y/%m/%d %H:%M:%S"

def unserialize_json_datetime(json_str):
    return datetime.strptime(json_str, DATEFORMAT)
    
def serialize_json_datetime(datetime_obj):
    return datetime.strftime(DATEFORMAT, datetime_obj)

class Request():
    """
    Request object that constructs a restful request
    """
    
    base_url = None
    request_type = None
    param = None
    data = None
    
    def __init__(self, base_url, request_type, param=None):
        """
        Constructor.
        request_type: Takes in any of the following 4 request methods (as string): "put", "delete", "post" and "get"
        data: Dictionary of data
        """
        self.base_url = base_url
        self.request_type = request_type
        self.set_param(param)
        REQ_CACHE[(base_url, request_type, hash(frozenset(param.items())))] = self
        
    @staticmethod
    def new(base_url, request_type, param=None):
        return REQ_CACHE.get((base_url, request_type, hash(frozenset(param.items()))) ,Request(base_url, request_type, param))
        
    def set_param(self, param):
        """
        Builds a data parameter from a dictionary of values
        """ 
        self.param = urlencode(param)
        
    
    def send(self, branch_url=None):
        """
        Makes the actual api call and saves the result as data
        """
        if branch_url == None: branch_url = ""
        
        if self.request_type.upper() == "GET":
            branch_url = branch_url + "?%s" % self.param
        
        connection =  httplib.HTTPSConnection(self.base_url)
        connection.request(self.request_type.upper(), branch_url, self.param)
        self.response = connection.getresponse()
        self.data = self.response.read()
        
    def json_data(self):
        if self.data:
            return loads(self.data)
        
    def decoded_data(self):
        """
        reverses a encoded string into a dict
        """
        sq = parse_qsl(self.data)
        return dict(sq)
        