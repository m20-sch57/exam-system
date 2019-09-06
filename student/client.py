"""
Contains client settings and server.
"""


import json
import socket
from xmlrpc.client import ServerProxy


class Client:
    """
    Contains client settings and server.
    """
    def __init__(self):
        self.path = 'client//settings.json'
        self.user = False
        self.user_name = 'Фёдор Куянов'
        self.password = '12345'
        # self.user_name = ''
        # self.password = ''
        self.salt = ':sdg436fregak'
        self.server = None
        self.update_server()

    def get_data(self):
        """
        Returns json data.
        """
        return json.load(open(self.path, 'r'))

    def set_data(self, data):
        """
        Assigns json data to data.
        """
        json.dump(data, open(self.path, 'w'), indent=4)

    def update_data(self, data):
        """
        Updates json data.
        """
        current_data = self.get_data()
        for key, value in data.items():
            current_data[key] = value
        self.set_data(current_data)

    def update_server(self):
        """
        Updates self.server.
        """
        self.server = ServerProxy('http://' + self.get_data()['server'])


socket.setdefaulttimeout(3)
