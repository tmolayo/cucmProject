from ldap3 import Connection, Server, ALL, MODIFY_REPLACE


class LdapConnection:
    def __init__(self, ldapServer, username, password):
        server = Server(ldapServer, get_info=ALL)
        self.connection = Connection(server, user=username, password=password)


    def getUserIPPhone(self, userName, connection):
        connection.bind()
        connection.search(search_base='search base', search_filter='(samAccountName=' + userName + ')',
                          attributes=['cn', 'samAccountName', 'ipPhone'])
        ipPhone = connection.response[0].get('attributes').get('ipPhone')
        connection.unbind()
        return ipPhone


    def getUserDN(self, userName, connection):
        connection.search(search_base='search base', search_filter='(samAccountName=' + userName + ')',
                          attributes=['cn', 'samAccountName', 'ipPhone'])
        return connection.response[0].get('dn')


    def setUserIPPhone(self, userName, ipPhone, connection):
        connection.bind()
        userDN = self.getUserDN(userName, connection)
        isModified = connection.modify(dn=userDN, changes={'ipPhone': [(MODIFY_REPLACE, [str(ipPhone)])]})
        connection.unbind()
        return isModified
