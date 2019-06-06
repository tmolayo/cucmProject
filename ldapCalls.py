from ldap3 import Connection, Server, ALL, MODIFY_REPLACE


class LdapConnection:
    def __init__(self, ldap_server, username, password):
        server = Server(ldap_server, get_info=ALL)
        self.connection = Connection(server, user=username, password=password)
        self.connection.bind()

    def get_user_ip_phone(self, user_name):
        self.connection.bind()
        self.connection.search(search_base='search base', search_filter='(samAccountName=' + user_name + ')',
                               attributes=['cn', 'samAccountName', 'ipPhone'])
        ip_phone = self.connection.response[0].get('attributes').get('ipPhone')
        if not ip_phone:
            return None
        else:
            return ip_phone

    def get_user_dn(self, user_name):
        self.connection.search(search_base='search base', search_filter='(samAccountName=' + user_name + ')',
                               attributes=['cn', 'samAccountName', 'ipPhone'])
        return self.connection.response[0].get('dn')

    def set_user_ip_phone(self, user_name, ip_phone):
        self.connection.bind()
        user_dn = self.getUserDN(user_name, self.connection)
        is_modified = self.connection.modify(dn=user_dn, changes={'ipPhone': [(MODIFY_REPLACE, [str(ip_phone)])]})
        return is_modified

    def __del__(self):
        self.connection.unbind()
        del self.connection
