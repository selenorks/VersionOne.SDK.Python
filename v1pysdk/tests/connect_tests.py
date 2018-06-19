import sys

from testtools import TestCase
from testtools.matchers import Equals

try:
    from xml.etree import ElementTree
    from xml.etree.ElementTree import parse, fromstring, Element
except ImportError:
    from elementtree import ElementTree
    from elementtree.ElementTree import parse, fromstring, Element

from v1pysdk.client import *
from .common_test_server import PublicTestServerConnection

class TestV1Connection(TestCase):
  def test_connect(self, username=None, password=None, address=None, instance=None):
    if not username and not password:
        username = PublicTestServerConnection.username
        password = PublicTestServerConnection.password
    if not address:
        address = PublicTestServerConnection.address
    if not instance:
        instance = PublicTestServerConnection.instance
    print("")
    print("Using Server: " + address + "/" + instance + ", User=" + username)
    
    server = V1Server(address=address, username=username, password=password,instance=instance)
    # The story names, but limit to only the first result so we don't get inundated with results
    code, body = server.fetch('/rest-1.v1/Data/Story?sel=Name&page=1,0')
    print("\n\nCode: ", code)
    print("Body: ", body)
    elem = fromstring(body)
    self.assertThat(elem.tag, Equals('Assets'))
