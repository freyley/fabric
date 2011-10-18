import unittest
from fabric.contrib.idp import Directory, GitRepository
from server import server, PASSWORDS, USER, HOST, PORT
from fabric.state import env
from fabric.network import to_dict

class IDPDirectoryTests(unittest.TestCase):

    def setUp(self):
       # Set up default networking for test server
        # we don't actually use this, but if we don't do it, tests ask questions on the command line
        env.disable_known_hosts = True
        env.update(to_dict('%s@%s:%s' % (USER, HOST, PORT)))
        env.password = PASSWORDS[USER]
        env.use_shell = False

    @server()
    def test_directory(self):
        d = Directory('/foo', commit=False, chmod='0777')
        self.assertEqual(['mkdir -p /foo', 'chmod 0777 /foo'], 
                         [unicode(c) for c in d.commands])
        d._exists = lambda x: True
        self.assertEqual(['rm /foo', 'mkdir /foo', 'chmod 0777 /foo'], 
                         [unicode(c) for c in d.commands])
        d._is_dir = lambda x: True
        self.assertEqual(['chmod 0777 /foo'], 
                         [unicode(c) for c in d.commands])
        cmdsrun = []
        def fake_run(cmd):
            cmdsrun.append(cmd)
        d = Directory('/foo', commit=False, owner="foo", chmod="0343", 
                      runcmd=fake_run, sudocmd=fake_run)
        d._exists = lambda x: True
        d.run()
        self.assertEqual(['rm /foo', 'mkdir /foo', 'chmod 0343 /foo', 'chown foo /foo'],
                         cmdsrun)
class IDPSymlinkTests(unittest.TestCase):
    pass

class IDPGitRepositoryTests(unittest.TestCase):
    pass


if __name__=='__main__':
    unittest.main()
