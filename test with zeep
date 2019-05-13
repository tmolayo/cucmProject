from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from lxml import etree


def show_history():
    for item in [history.last_sent, history.last_received]:
        print(etree.tostring(item["envelope"], encoding="unicode", pretty_print=True))

def getLineUuid(lineId):
    lineJson = None
    try:
        lineJson = client.service.getLine(pattern=lineId, returnedTags={'_uuid': True})
    except Exception as error:
        if (error.fault.faultstring == "Item not valid: The specified Line was not found"):
            return None
        else:
            raise (error)
    return lineJson['return']['line']['_uuid']


disable_warnings(InsecureRequestWarning)
username = 'administrator'
password = 'ciscopsdt'

# If you're not disabling SSL verification, host should be the FQDN of the server rather than IP
host = '10.10.20.1'
wsdl = 'file://schema/AXLAPI.wsdl'
location = 'https://{host}:8443/axl/'.format(host=host)
binding = "file://schema/AXLSoap.xsd"

# Create a custom session to disable Certificate verification.
# In production you shouldn't do this,
# but for testing it saves having to have the certificate in the trusted store.
session = Session()
# session.verify = False
session.auth = HTTPBasicAuth(username, password)
transport = Transport(cache=SqliteCache(), session=session, timeout=20)
history = HistoryPlugin()
# client = Client(wsdl=wsdl, transport=transport, plugins=[history])
client = Client(wsdl=wsdl, transport=transport)
service = client.create_service(binding, location)

print(getLineUuid('1001'))








# def dean(*a):
#     print(a)
#
# b = ['a', 'b', 'c','d']
#
# dean(b)
# dean(*b)