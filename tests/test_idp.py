import unittest
from fabric.contrib.idp import *

class IDPDirectoryTests(unittest.TestCase):
    def test_directory(self):
        d = Directory('/foo', commit=False, chmod='0777')
        self.assertEqual('', d.commands)

if __name__=='__main__':
    unittest.main()
