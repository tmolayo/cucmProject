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

def addUser(userId, firstName, lastName, devices=None):
    if (devices == None or len(devices) == 0):
        response = client.service.addUser(
            user={
                'firstName': firstName,
                'lastName': lastName,
                'userid': userId,
                'presenceGroupName': 'Standard Presence group'
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

def getUserInfo(userId):
    """Get all the information of the user, raise exception if he did not found"""
    if(not searchForUser(userId)):
        raise RuntimeError('The user id not exist, the user id=> ' + userId)
    else:
        return client.service.getUser(userid=userId)['return']['user']

def searchForUser(userId, attributes=['uuid']):
    """ search for user, if he not found return None else
        return by default his uuid or the inputs attributes"""
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
    return searchForUser(userId)['uuid']

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

def addPhoneWithLine(phoneName, lineId):
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

def searchForPhone(phoneName, attributes=['uuid']):
    """ search for user, if he not found return None else
        return by default his uuid or the inputs attributes"""
    returnedTagsForApi = {}
    for attr in attributes:
        returnedTagsForApi[attr] = True
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
    return searchForPhone(phoneName)['uuid']

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
    return client.service.addLine(line={
        'pattern': id,
        'usage':'',
        'description' : 'description' + id,
        'alertingName' : 'alertingName' + id,
        'routePartitionName': None})['return']

def searchForLine(lineId, attributes=['uuid']):
    """ search for user, if he not found return None else
        return by default his uuid or the inputs attributes"""
    returnedTagsForApi = {}
    for attr in attributes:
        returnedTagsForApi[attr] = True
    lineJson = client \
        .service.listLine(searchCriteria={'pattern': lineId}, returnedTags=returnedTagsForApi)
    if(not lineJson['return'] or not lineJson['return']['line'] ):
        return None
    if (len(lineJson['return']['line']) > 1):
        raise ValueError('found more then one line with the same id, the id => ' + lineId)
    return lineJson['return']['line'][0]

def getLineUuid(lineId):
    return searchForLine(lineId)['uuid']

def updateUserSelfSerivce(userId, selfServiceUserID):
    return client.service.updateUser(userid=userId, selfService=selfServiceUserID)

def updateUserSelfSerivce(userID, selfServiceUserID):
    return client.service.updateUser(userid=userID, selfService=selfServiceUserID)

def addAssociateDeviceToUser(userId, newDevice):
    oldDevices = getUserInfo(userId)['associatedDevices']
    userDevices = [newDevice]
    if(oldDevices and oldDevices['device']):
        userDevices += oldDevices['device']
    return client.service.updateUser(userid=userId, associatedDevices={'device': userDevices})

def updatePrimaryExtentionToUser(userId,lineId):
    return client.service.updateUser(userid=userId,
                                     primaryExtension={'pattern': lineId})

def checkPart1():
    line = '1037'
    userName = 'deanTest7'
    phoneName = 'deanTest107'
    addUser(userName, 'dean', 'bachar')
    updateUserSelfSerivce(userName, line)
    addLine(line)
    addPhoneWithLine(phoneName, line)
    addAssociateDeviceToUser(userName, 'CSF' + phoneName)
    updatePrimaryExtentionToUser(userName, line)

disable_warnings(InsecureRequestWarning)
username = 'administrator'
password = 'ciscopsdt'

# If you're not disabling SSL verification, host should be the FQDN of the server rather than IP
wsdl = 'file://schema/AXLAPI.wsdl'
client = getAuthenticationWithServer(username, password, wsdl)


