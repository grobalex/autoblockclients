#! /opt/local/bin/python2.7

import requests
import base64
import json
import logging
logging.captureWarnings(True)

class FortiPortalREST:
    def __init__(self):
        self._debug = False
        self.s = requests.Session()
        self.headers = {
            "Content-Type": "application/json",
        }
        self.s.headers.update(self.s.headers)
        self.base_url = "https://{}/fpc/api"

    def login(self, ip, login, password):
        self.base_url = self.base_url.format(ip)
        url = self.base_url + "/login"
        data = {
            "user": login,
            "password": password,
        }
        r = self.s.post(url, json=data, verify=False)

        self.debug_print(r)
        
        response = r.json()

        self.sid = response["fpc-sid"]
        self.headers["fpc-sid"] = self.sid
        self.s.headers.update(self.headers)

    def logout(self):
        url = self.base_url + "/logout"
        r = self.s.post(url)

        self.debug_print(r)

    def debug(self, value):
        if value == 'on':
            self._debug = True
        else:
            self._debug = False

    def get(self, endpoint):
        endpoint = endpoint.strip('/')
        url = "{}/{}".format(self.base_url, endpoint)
        r = self.s.get(url)

        self.debug_print(r)

        return r

    def post(self, endpoint, data):
        endpoint = endpoint.strip('/')        
        url = "{}/{}".format(self.base_url, endpoint)        

        r = self.s.post(url, json=data)

        self.debug_print(r)

        return r
        
    def debug_print(self, response):
        if self._debug:
            # Print the request:
            method = response.request.method
            url = response.request.url
            print("==> REQUEST:\n\n{} {}".format(method, url))
            for key in response.request.headers:
                value = response.request.headers[key]
                print("{}: {}".format(key, value))

            body_request = response.request.body

            if body_request != None:
                try:
                    json_object = json.loads(body_request)
                except ValueError:
                    print("\n{}".format(body_request))
                else:
                    print("\n{}".format(json.dumps(json_object, indent=4)))

            # Print the response:
            print("\n==> RESPONSE: \n")
            print(response.status_code)
            for key in response.headers:
                value = response.headers[key]
                print("{}: {}".format(key, value))

            try:
                json_object = response.json()
            except ValueError:
                pass
            else:
                print("\n{}".format(json.dumps(json_object, indent=4)))
        
if __name__ == '__main__':

    ip = "10.210.35.195"
    #ip = "10.220.64.120"
    login = "spuser"
    password = "test123"

    fpc = FortiPortal()
    fpc.debug('on')
    fpc.login(ip, login, password)

    endpoint = 'customers'
    data = {
        "customerName": "Tenant 16",
        "address1": "20 William Pickering Dr",
        "address2": "Albany",
        "city": "Auckland",
        "zip": "0632",
        "phone": "006494228638",
        "fax": "006494228639",
        "contactFname": "Test",
        "contactLname": "Tenant3",
        "contactEmail": "tenant3@rvn.mgmt",
        "totalStorage": 5,
    }        

    fpc.post(endpoint, data)
    fpc.debug('off')
    fpc.logout()
    
