#-- unit tests that needs automation --#

#from api.test_user import UserTests
#from tests.action.test_share import ShareTests

#-- working unit tests --#

from tests.action.test_checkpoint import CheckpointTests
from tests.action.test_location import LocationTests
from tests.api.test_checkpoint import CheckpointAPITests
from tests.api.test_catalog import CatalogAPITests
from tests.api.test_share import ShareAPITest
from tests.api.test_like import LikeAPITest
from tests.api.test_comment import CommentAPITest

import unittest

if __name__ == "__main__":
    unittest.main()