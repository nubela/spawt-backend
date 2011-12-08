#===============================================================================
# unit tests for location action layer
#===============================================================================
from tests.test_base import TestBase
from action.location import add_location, get_location

class LocationTests(TestBase):
    
    def test_add_location(self):
        """
        unit test for add_location functionality
        """
        location = add_location(2.0, 3.0)
        assert not get_location(location.id) is None