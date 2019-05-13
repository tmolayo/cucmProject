from pip._vendor.pyparsing import unicode_set
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
import ssl

def getAuthenticationWithServer(username, password,wsdl):
    session = Session()
    session.verify = False
    session.auth = HTTPBasicAuth(username, password)
    transport = Transport(cache=SqliteCache(), session=session, timeout=20)
    history = HistoryPlugin()
    ssl._create_default_https_context = ssl._create_unverified_context
    return (Client(wsdl=wsdl, transport=transport, plugins=[history]))


def show_history():
    for item in [history.last_sent, history.last_received]:
        print(etree.tostring(item["envelope"], encoding="unicode", pretty_print=True))

def getLineUuid(lineId):
    lineJson = None
    try:
        lineJson = client.service.getLine(pattern=lineId, returnedTags={'_uuid': ''})
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
wsdl = 'file://schema/AXLAPI.wsdl'
client = getAuthenticationWithServer(username, password, wsdl)
print(client.service.updateUser(userid='dean', selfService='999999'))
# binding = "file://schema/AXLSoap.xsd"

# Create a custom session to disable Certificate verification.
# In production you shouldn't do this,
# but for testing it saves having to have the certificate in the trusted store.
# session = Session()
# session.verify = False
# session.auth = HTTPBasicAuth(username, password)
# transport = Transport(cache=SqliteCache(), session=session, timeout=20)
# history = HistoryPlugin()
# ssl._create_default_https_context = ssl._create_unverified_context
# client = Client(wsdl=wsdl, transport=transport, plugins=[history])
# print(client.service.getLine(pattern="1021"))
# ssl._create_default_https_context = ssl._create_unverified_context
# client = Client(wsdl=wsdl, transport=transport)
# service = client.create_service(binding, location)

# print(getLineUuid('1021'))








# def dean(*a):
#     print(a)
#
# b = ['a', 'b', 'c','d']
#
# dean(b)
# dean(*b)