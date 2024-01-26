import json

import requests


class McDisher:
    logged_in: bool = False
    s = requests.Session()

    def login(self, username: str, password: str) -> bool:
        if self.logged_in:
            return True

        url = 'http://localhost:8000/accounts/login/'
        obj = {'username': username,
               'password': password}

        x = self.s.post(url, data=obj, verify=False)
        print(f"Status: {x.status_code}")
        if x.status_code == 200:
            self.logged_in = True
            return True

        print("Cannot log in")
        return False

    def request(self, device: str, meta_string: str) -> object:
        """
        Request a MAC address\n
        Returns None on failure\n
        The returned object will have the following values:\n
        'id', 'mac', 'user', 'device', 'metastring', 'time', 'allocation'
        :param device: Device name
        :param meta_string: Metadata about device
        :return object: An object containing the PENDING MAC
        """
        url = "http://localhost:8000/macdisher/getMAC/"
        obj = {'device': device,
               'metastring': meta_string}
        x = self.s.post(url, json=obj)
        print(f"Status: {x.status_code}")
        print(x.text)
        if x.status_code == 200:
            return json.loads(x.text)

    def assign(self, mac: str) -> bool:
        """
        Assign a MAC to device.
        This will change the MAC from PENDING to ASSIGNED
        :param mac: MAC address that should be assigned
        :return: True
        """
        url = "http://localhost:8000/macdisher/assignMAC/"
        obj = {'macs': [mac]}
        x = self.s.post(url, json=obj)
        print(f"Status: {x.status_code}")
        print(x.text)
        if x.status_code == 200:
            return True


print("Running python 3")
McDisherObject= McDisher()
username='student1'
password='IAmAStudentHere'
McDisherObject.login(username,password)

Device="COMS_UNIT"
MetaString="Testing Python script3.2"
macs=McDisherObject.request(Device,MetaString)

mac=(macs[0]['mac'])
print(mac)
McDisherObject.assign(mac)