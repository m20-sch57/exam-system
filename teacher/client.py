"""
Contains client settings and server.
"""


import os
import socket
from xmlrpc.client import ServerProxy


class Client:
    """
    Contains client settings and server.
    """
    def __init__(self):
        self.path = os.path.join('client')
        self.user = False
        self.user_name = 'Админ'
        self.password = '12345'
        # self.user_name = ''
        # self.password = ''
        self.update_server()

    def get_item(self, item):
        """
        Returns value of the item.
        """
        return open(os.path.join(self.path, item), encoding='utf-8-sig').read()

    def set_item(self, item, value):
        """
        Sets value of the item.
        """
        open(os.path.join(self.path, item), 'w', encoding='utf-8-sig').write(value)

    def get_settings(self):
        """
        Returns map of all settings.
        """
        settings = {}
        for item in os.listdir(self.path):
            settings[item] = self.get_item(item)
        return settings

    def update_server(self):
        """
        Updates self.server.
        """
        self.server = ServerProxy('http://' + self.get_item('server'))


socket.setdefaulttimeout(3)
