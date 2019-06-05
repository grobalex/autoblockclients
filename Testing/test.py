import unittest
import requests
import getpass

class Tests(unittest.TestCase):

    def send_post(api, data):
        return requests.post("http://127.0.0.1:5000/" + api , data=data, headers={'content-type': "application/json"}).json()["Status"]

    def test_API(self):
        # successfully added
        self.assertEqual(Tests.send_post("block", {'ip': "240.1.1.1"}), "Success")
        # add to do not block table
        self.assertEqual(Tests.send_post("add", {'ip': "242.1.1.1"}), "Success")
        # add to do not block table again
        self.assertEqual(Tests.send_post("add", {'ip': "242.1.1.1"}), "1062 Duplicate entry 242.1.1.1 for key ipUNIQUE")
        # on do not block table
        self.assertEqual(Tests.send_post("block", {'ip': "242.1.1.1"}), "Error - Cannot block this IP")
        # duplicate request
        self.assertEqual(Tests.send_post("block", {'ip': "240.1.1.1"}), "1062 Duplicate entry 127.0.0.1-240.1.1.1 for key uniqueindex")

if __name__ == '__main__':
    unittest.main()
