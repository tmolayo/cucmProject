from os.path import abspath
from urllib.parse import urljoin
from urllib.request import pathname2url
import ssl
from suds.client import Client

def getAuthenticationWithServer(ip, username, password,WSDL):
    if hasattr(ssl, '_create_unverified_context'):
        print("allow insecure connections")
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

def getPhone(client, name):
    return (client.service.getPhone(name=name)['return']['phone'])

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
def addLine(id):
    print('start adding line which name ' + id)
    objectId =  client.service.addLine(line={
        'pattern': id,
        'description' : 'description' + id,
        'alertingName' : 'alertingName' + id,
        'routePartitionName': 'Global Learned E164 Patterns'})
    print('end adding line which name ' + id)
    return objectId

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
idLine = addLine(shluha)['return']
print('add a phone')
addPhoneWithLine(client, phoneName, idLine)

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
