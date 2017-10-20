#!/usr/bin/env python3

import unittest
from websvc import CheckUrl

class TestCheckUrl(unittest.TestCase):

    def setUp(self):
        self.service = CheckUrl()

    def test_get_ok(self):
        self.service.get('google.com:80/')

    def test_get_bad(self):
        self.service.get('')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
