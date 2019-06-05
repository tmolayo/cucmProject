from ldap3 import Connection, Server, ALL, MODIFY_REPLACE


class LdapConnection:
    def __init__(self, ldap_server, username, password):
        server = Server(ldap_server, get_info=ALL)
        self.connection = Connection(server, user=username, password=password)
        self.connection.bind()

    @staticmethod
    def get_user_ipphone(user_name, connection):
        connection.bind()
        connection.search(search_base='search base', search_filter='(samAccountName=' + user_name + ')',
                          attributes=['cn', 'samAccountName', 'ipPhone'])
        ip_phone = connection.response[0].get('attributes').get('ipPhone')
        return ip_phone

    @staticmethod
    def get_user_dn(user_name, connection):
        connection.search(search_base='search base', search_filter='(samAccountName=' + user_name + ')',
                          attributes=['cn', 'samAccountName', 'ipPhone'])
        return connection.response[0].get('dn')

    def set_user_ip_phone(self, user_name, ip_phone, connection):
        connection.bind()
        user_dn = self.getUserDN(user_name, connection)
        is_modified = connection.modify(dn=user_dn, changes={'ipPhone': [(MODIFY_REPLACE, [str(ip_phone)])]})
        return is_modified

    def end_connection(self):
        self.connection.unbind()
        del self.connection
