from ldap3 import Connection, Server, ALL, MODIFY_REPLACE
import json

with open('./configuration/info.json', 'r') as file:
    info = json.load(file)

server = Server(info['prod']['DC'], get_info=ALL)
connection = Connection(server, user=info['prod']['credentials']['username'],
                        password=info['prod']['credentials']['password'])


def getUserIPPhone(userName):
    connection.bind()
    connection.search(search_base='search base', search_filter='(samAccountName=' + userName + ')',
                      attributes=['cn', 'samAccountName', 'ipPhone'])
    return connection.response[0].get('attributes').get('ipPhone')
    connection.unbind()

def getUserDN(userName):
    connection.search(search_base='search base', search_filter='(samAccountName=' + userName + ')',
                      attributes=['cn', 'samAccountName', 'ipPhone'])
    return connection.response[0].get('dn')


def setUserIPPhone(userName, ipPhone):
    connection.bind()
    userDN = getUserDN(userName)
    return connection.modify(dn=userDN, changes={'ipPhone': [(MODIFY_REPLACE, [str(ipPhone)])]})
    connection.unbind()
