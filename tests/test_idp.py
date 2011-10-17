import unittest
from fabric.contrib.idp import Directory, GitRepository
from server import server, PASSWORDS, USER, HOST, PORT
from fabric.state import env
from fabric.network import to_dict

class IDPDirectoryTests(unittest.TestCase):

    def setUp(self):
       # Set up default networking for test server
        env.disable_known_hosts = True
        env.update(to_dict('%s@%s:%s' % (USER, HOST, PORT)))
        env.password = PASSWORDS[USER]
        # Command response mocking is easier without having to account for
        # shell wrapping everywhere.
        env.use_shell = False

    @server()
    def test_directory(self):
        d = Directory('/foo', commit=False, chmod='0777')
        self.assertEqual(['mkdir -p /foo', 'chmod 0777 /foo'], 
                         [unicode(c) for c in d.commands])
        d.exists = lambda x: True
        self.assertEqual(['rm /foo', 'mkdir /foo', 'chmod 0777 /foo'], 
                         [unicode(c) for c in d.commands])
        d.is_dir = lambda x: True
        self.assertEqual(['chmod 0777 /foo'], 
                         [unicode(c) for c in d.commands])

if __name__=='__main__':
    unittest.main()
