from testtools import TestCase
from testtools.matchers import Equals
from testtools.content import text_content

# try the old version, then fallback to the new one
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
    self.addDetail('URL', text_content(address + "/" + instance))
    self.addDetail('username', text_content(username))

    server = V1Server(address=address, username=username, password=password,instance=instance)
    # The story names, but limit to only the first result so we don't get inundated with results
    code, body = server.fetch('/rest-1.v1/Data/Story?sel=Name&page=1,0')
    self.addDetail('Code', text_content(str(code)))
    self.addDetail('Body', text_content(str(body)))

    elem = fromstring(body)
    self.assertThat(elem.tag, Equals('Assets'))
