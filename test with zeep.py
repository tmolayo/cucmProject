#from pip._vendor.pyparsing import unicode_set
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


def updateUserSelfSerivce(userID, selfServiceUserID):
    try:
        return client.service.updateUser(userid=userID, selfService=selfServiceUserID)
    except Exception as error:
        return error


# TODO: Unable to associate more that one device
def associateDevice(userID, device):
    try:
        return client.service.updateuser(userid=userID, associatedDevices=device)
    except Exception as error:
        return error


disable_warnings(InsecureRequestWarning)
username = 'administrator'
password = 'ciscopsdt'

# If you're not disabling SSL verification, host should be the FQDN of the server rather than IP
wsdl = 'file://schema/AXLAPI.wsdl'
client = getAuthenticationWithServer(username, password, wsdl)
