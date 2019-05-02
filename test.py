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
#print (getUsers(client)['return']['user'])
addUser(client, "1105", "gilad", "livne", ["CSFUSER001"])
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
