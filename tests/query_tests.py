
from testtools import TestCase

import v1pysdk
from .common_test_server import PublicTestServerConnection

class TestV1Query(TestCase):
    def test_select_story(self):
        with PublicTestServerConnection.getV1Meta() as v1:
            obtainedAll=True
            try:
                for t in v1.AssetType.select('Name').where(Name='Story').page(size=5):
                    print(t)
            except:
                obtainedAll=False

            self.assertEqual(obtainedAll, True)
