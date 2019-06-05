import requests
import getpass

test = {'ip': "220.1.1.1"}

print(requests.post("http://127.0.0.1:5000/block", data=test,
                    headers={'content-type': "application/json"}).json())
