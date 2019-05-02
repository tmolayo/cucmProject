from os.path import abspath
from urllib.parse import urljoin
from urllib.request import pathname2url
import ssl
from suds.client import Client

cucmIp = '10.10.20.1'
cucmUsername = 'administrator'
cucmPassword = 'ciscopsdt'
WSDL = urljoin('file:', pathname2url(abspath('schema/AXLAPI.wsdl')))

# Allow insecure connections
if hasattr(ssl, '_create_unverified_context'):
    print("allow insecure connections")
    ssl._create_default_https_context = ssl._create_unverified_context

CLIENT = Client(WSDL, location='https://%s:8443/axl/' % (cucmIp),
                username=cucmUsername, password=cucmPassword)
response = None
try:
    response = CLIENT.service.listUser(
        searchCriteria={
            'userid': '%'
        },
        returnedTags={
            'userid': True,
            'telephoneNumber': True,
            'lastName': True
        })
    print(response['return']['user'])

except Exception:
    print('error ')
