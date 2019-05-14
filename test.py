from os.path import abspath
from urllib.parse import urljoin
from urllib.request import pathname2url
import ssl
from suds.client import Client
from suds import *

# ToDo: function that get value from json and raise exception if the json not in the right convention
def getFromJson(json, arrOfAttributes):
    pass

def getAuthenticationWithServer(ip, username, password,WSDL):
    # if hasattr(ssl, '_create_unverified_context'):
    #     print("allow insecure connections")
    ssl._create_default_https_context = ssl._create_unverified_context
    return (Client(WSDL, location='https://%s:8443/axl/' % (ip),
                   username=username, password=password))

def getUsers(client):
    response = client.service.listUser(
        searchCriteria={
            'userid': '%'
        },
        returnedTags={
            'userid': True,
            'telephoneNumber': True,
            'lastName': True
        })
    return (response)

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

# ToDo: handleing phone not found and the json is not in the right convention
def getPhone(name):
    return (client.service.getPhone(name=name)['return']['phone'])

# Update the first line of the phone and erase the others
def updatePhoneLine(phoneName, lineId):
    lineUuid = getLineUuid(lineId)
    if(lineUuid == None):
        raise ValueError("The Line " + lineId + ' not exist')
    client.service.updatePhone(name=phoneName, lines={
        'line': {
            'index': 1,
            'dirn': {
                '_uuid': lineUuid
            },
            'display': 'displayCheck',
            'label': 'labelCheck'
        }})

# Get the uuid of the line by line id, return None if the line not found
def getLineUuid(lineId):
    lineJson = None
    try:
        lineJson = client.service.getLine(pattern=lineId, returnedTags={'_uuid': True})
    except WebFault as error:
        if (error.fault.faultstring == "Item not valid: The specified Line was not found"):
            return None
        else:
            raise (error)
    return lineJson['return']['line']['_uuid']

# Get the uuid of the phone by phone name, return None if the phone not found
def getPhoneUuid(phoneName):
    phoneJson = None
    try:
        phoneJson = client.service.getPhone(name=phoneName, returnedTags={'_uuid': True})
    except WebFault as error:
        if (error.fault.faultstring == 'Item not valid: The specified ' + phoneName +' was not found'):
            return None
        else:
            raise (error)
    return phoneJson['return']['phone']['_uuid']

def isLineExist(lindId):
    return (getLineUuid(lindId) != None)

 # not working
def copyPhone(client, copiedPhoneName, newPhoneName):
    copiedPhone = getPhone(client, copiedPhoneName)
    client.service.addPhone(phone={
        'name': '%s%s' % ('CSF', copyPhone),
        'product': copiedPhone.product,
        'class': 'Phone',
        'protocol': 'SIP',
        'protocolSide': 'User',
        'devicePoolName': 'Default',
        'sipProfileName':
            'Standard SIP Profile',
    })

def addPhone(client):
    client.service.addPhone(phone={
        'name': '%s%s' % ('CSF', 'dean00005'),
        'product': 'Cisco Unified Client Services Framework',
        'class': 'Phone',
        'protocol': 'SIP',
        'protocolSide': 'User',
        'devicePoolName': 'Default',
        'sipProfileName':
            'Standard SIP Profile',
    })

# Todo: handleing error on json we got
# return the line uuid
def addLine(id):
    print('start adding line which name ' + id)
    objectId =  client.service.addLine(line={
        'pattern': id,
        'description' : 'description' + id,
        'alertingName' : 'alertingName' + id,
        'routePartitionName': 'Global Learned E164 Patterns'})
    print('end adding line which name ' + id)
    return objectId['return']

def addPhoneWithLine(client, phoneName, lineId):
    client.service.addPhone(phone={
        'name': '%s%s' % ('CSF', phoneName),
        'product': 'Cisco Unified Client Services Framework',
        'class': 'Phone',
        'protocol': 'SIP',
        'protocolSide': 'User',
        'devicePoolName': 'Default',
        'sipProfileName': 'Standard SIP Profile',
        'lines': {
            'line': {
                'index': 1,
                'dirn': {
                    '_uuid': lineId
                },
                'display': 'displayCheck',
                'label': 'labelCheck'

            }},
    })

#not Working!
def isUserExist(client, userid):
    print("checking if " + userid + " exist")
    response = client.service.listUser(
        searchCriteria={
            'userid': userid
        },
        returnedTags={
            'userid': True
        })

    return (response['return'] != None and response['return']['user'])


cucmIp = '10.10.20.1'
cucmUsername = 'administrator'
cucmPassword = 'ciscopsdt'
WSDL = urljoin('file:', pathname2url(abspath('schema/AXLAPI.wsdl')))
client = getAuthenticationWithServer(cucmIp, cucmUsername, cucmPassword, WSDL)
shluha = '1000013'
phoneName = 'dean0013'
# client.service.getLine(pattern="1021")
# print(client.service.getLine(pattern='1022', returnedTags={'_uuid': True}))
print(client.service.getLine(pattern='1027', returnedTags={'_uuid': True}))
# print(getPhoneUuid('CSFUSER002222'))

# print('is line 1021 exist => ' + (str)(isLineExist('1021')))
# print('is line 1022 exist => ' + ((str)(isLineExist('1022'))))
# try:
#     getLineUuid('1022')
# except WebFault as error:
#     if (error.fault.faultstring == "Item not valid: The specified Line was not found"):
#         print('okokokok')
#     else:
#         raise(error)
# idLine = addLine(shluha)['return']
# print('add a phone')
# addPhoneWithLine(client, phoneName, idLine)

#copyPhone(client, "CSFTemp", "CSFtest001")

# addPhone(client)
#print(getPhone(client,'CSFTemp'))
#print (getUsers(client)['return']['user'])
# addUser(client, "1105", "gilad", "livne", ["CSFUSER001"])
#print (getUsers(client)['return']['user'])
# print (getUsers(client)['return']['user'][0]['userid'])
# print (isUserExist(client, "dean"))

# WSDL = urljoin('file:', pathname2url(abspath('schema/AXLAPI.wsdl')))
# # Allow insecure connections
# if hasattr(ssl, '_create_unverified_context'):
#     print("allow insecure connections")
#     ssl._create_default_https_context = ssl._create_unverified_context
#
# CLIENT = Client(WSDL, location='https://%s:8443/axl/' % (cucmIp),
#                 username=cucmUsername, password=cucmPassword)
# response = None
# try:
#     response = CLIENT.service.listUser(
#         searchCriteria={
#             'userid': '%'
#         },
#         returnedTags={
#             'userid': True,
#             'telephoneNumber': True,
#             'lastName': True
#         })
#     print(response['return']['user'])
#     print(response)
#
# except Exception:
#     print("EXCEPTION")
#     print(response)
