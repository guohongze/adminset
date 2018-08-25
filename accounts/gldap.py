#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ldap3 import Server, Connection, SUBTREE
from lib.common import get_dir


class UseLdap:
    def __init__(self):
        self.port = get_dir("ldap_port")
        self.server = get_dir("ldap_server")
        self.manager = get_dir("ldap_manager")
        self.passwd = get_dir("ldap_password")
        self.base = get_dir("base_dn")
        self.type = get_dir("ldap_filter")
        if self.port:
            self.server = self.server + ":" + self.port

    def connect(self):
        server = Server(self.server)
        c = Connection(server, user=self.manager, password=self.passwd)
        c.bind()
        return c

    def get_dn(self, username):
        if self.type == "OpenLDAP":
            ldap_type = "uid"
        else:
            ldap_type = "sAMAccountName"
        c = self.connect()
        c.search(search_base=self.base,
                 search_filter="(&(objectClass=*)({0}={1}))".format(ldap_type, username),
                 search_scope=SUBTREE
                 )
        for entry in c.response:
            user_dn = entry['dn']
        c.unbind()
        return user_dn

    def change_password(self, username, newpwd):
        user_dn = self.get_dn(username)
        c = self.connect()
        if self.type == "OpenLDAP":
            c.extend.standard.modify_password(user_dn, new_password=newpwd)
        else:
            c.extend.microsoft.modify_password(user_dn, new_password=newpwd)
        c.unbind()


def change_ldap_passwd(username, newpwd):
    g = UseLdap()
    g.change_password(username, newpwd)
    return "OK"

