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
    disable_warnings(InsecureRequestWarning)
    session = Session()
    session.verify = False
    session.auth = HTTPBasicAuth(username, password)
    transport = Transport(cache=SqliteCache(), session=session, timeout=20)
    history = HistoryPlugin()
    ssl._create_default_https_context = ssl._create_unverified_context
    return (Client(wsdl=wsdl, transport=transport, plugins=[history]))

def addUser(client,userId, firstName, lastName, devices):
    if (devices == None or len(devices) == 0):
        response = client.service.addUser(
            user={
                'firstName': firstName,
                'lastName': lastName,
                'userid': userId
            })
    else:
        dictDevices = []
        for device in devices:
            dictDevices.append({'device': device})
        print(dictDevices)
        response = client.service.addUser(
            user={
                'firstName': firstName,
                'lastName': lastName,
                'userid': userId,
                'associatedDevices': dictDevices
            })

def getUserInfo(userId, attributes=[]):
    """ Get info about of the user by user id,
      return None if the user not found, if more then 1 found raise exception"""
    returnedTagsForApi = {}
    for attr in attributes:
        returnedTagsForApi[attr] = ''
    userJson = client.service \
        .listUser(searchCriteria={'userid': userId}, returnedTags=returnedTagsForApi)
    if (not userJson['return'] or not userJson['return']['user'] ):
        return None
    if (len(userJson['return']['user']) > 1):
        raise RuntimeError('found more then one user with the same id, the id => ' + userId)
    return userJson['return']['user'][0]

def getUserUuid(userId):
    """ Get uuid about of the user by user id,
         return None if the user not found, if more then 1 found raise exception"""
    return getPhoneInfo(userId, attributes=['uuid'])['uuid']

def addPhone(client, name):
    client.service.addPhone(phone={
        'name': '%s%s' % ('CSF', name),
        'product': 'Cisco Unified Client Services Framework',
        'class': 'Phone',
        'protocol': 'SIP',
        'protocolSide': 'User',
        'devicePoolName': 'Default',
        'sipProfileName': 'Standard SIP Profile',
        'commonPhoneConfigName': 'Standard Common Phone Profile',
        'locationName': 'Hub_None'
    })

def addPhoneWithLine(client, phoneName, lineId):
    lineUuid = getLineUuid(lineId)
    if (not lineUuid):
        raise ValueError('The line with the id ' + lineUuid + ' is not exist')
    client.service.addPhone(phone={
        'name': '%s%s' % ('CSF', phoneName),
        'product': 'Cisco Unified Client Services Framework',
        'class': 'Phone',
        'protocol': 'SIP',
        'protocolSide': 'User',
        'devicePoolName': 'Default',
        'sipProfileName': 'Standard SIP Profile',
        'commonPhoneConfigName': 'Standard Common Phone Profile',
        'locationName': 'Hub_None',
        'lines': {
            'line': {
                'index': 1,
                'dirn': {
                    'uuid': lineUuid,
                    'pattern': lineId
                },
                'display': 'displayCheck',
                'label': 'labelCheck'

            }},
    })

def getPhoneInfo(phoneName, attributes=[]):
    """ Get info about of the phone by phone name,
    return None if the phone not found, if more then 1 found raise exception"""
    returnedTagsForApi = {}
    for attr in attributes:
        returnedTagsForApi[attr] = ''
    phoneJson = client.service\
        .listPhone(searchCriteria={'name': '%s%s' % ('CSF', phoneName)}, returnedTags=returnedTagsForApi)
    if (not phoneJson['return'] or not phoneJson['return']['phone']):
        return None
    if (len(phoneJson['return']['phone']) > 1):
        raise RuntimeError('found more then one phone with the same name, the name => ' + phoneName)
    return phoneJson['return']['phone'][0]

def getPhoneUuid(phoneName):
    """ Get uuid about of the phone by phone name,
        return None if the phone not found, if more then 1 found raise exception"""
    return getPhoneInfo(phoneName, attributes=['uuid'])['uuid']

def updatePhoneLine(phoneName, lineId):
    """update the line of a phone"""
    lineUuid = getLineUuid(lineId)
    if (not lineUuid):
        raise ValueError('The line with the id ' + lineUuid + ' is not exist')
    client.service.updatePhone(name= '%s%s' % ('CSF', phoneName), lines={
        'line': {
            'index': 1,
            'dirn': {
                'uuid': lineUuid,
                'pattern': lineId
            },
            'display': 'displayCheck',
            'label': 'labelCheck'
        }})

def addLine(id):
    """add a line"""
    return  client.service.addLine(line={
        'pattern': id,
        'usage':'',
        'description' : 'description' + id,
        'alertingName' : 'alertingName' + id,
        'routePartitionName': 'Global Learned E164 Patterns'})['return']

def getLineInfo(lineId, attributes=[]):
    """ Get the uuid of the line by line id,
    return None if the line not found, raise exception if more then one founded"""
    returnedTagsForApi = {}
    for attr in attributes:
        returnedTagsForApi[attr] = ''
    lineJson = client \
        .service.listLine(searchCriteria={'pattern': lineId}, returnedTags=returnedTagsForApi)
    if(not lineJson['return'] or not lineJson['return']['line'] ):
        return None
    if (len(lineJson['return']['line']) > 1):
        raise RuntimeError('found more then one line with the same id, the id => ' + lineId)
    return lineJson['return']['line'][0]

def getLineUuid(lineId):
    return getLineInfo(lineId, attributes=['uuid'])['uuid']

# ToDo: function that get value from json and raise exception if the json not in the right convention
def getFromJson(json, arrOfAttributes):
    pass


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