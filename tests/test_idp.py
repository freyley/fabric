import unittest
from fabric.contrib.idp import Directory, GitRepository, Symlink
from server import server, PASSWORDS, USER, HOST, PORT
from fabric.state import env
from fabric.network import to_dict

class FabricTestCase(unittest.TestCase):
    def setUp(self):
       # Set up default networking for test server
        # we don't actually use this, but if we don't do it, tests ask questions on the command line
        env.disable_known_hosts = True
        env.update(to_dict('%s@%s:%s' % (USER, HOST, PORT)))
        env.password = PASSWORDS[USER]
        env.use_shell = False
    
    def cmdstostr(self, commands):
        return [unicode(c) for c in commands]   


class IDPDirectoryTests(FabricTestCase):

    @server()
    def test_directory(self):
        d = Directory('/foo', commit=False, chmod='0777')
        self.assertEqual(['mkdir -p /foo', 'chmod 0777 /foo'], 
                         self.cmdstostr(d.commands))
        d._exists = lambda x: True
        self.assertEqual(['rm /foo', 'mkdir /foo', 'chmod 0777 /foo'], 
                         self.cmdstostr(d.commands))
        d._is_dir = lambda x: True
        self.assertEqual(['chmod 0777 /foo'], 
                         self.cmdstostr(d.commands))
        cmdsrun = []
        def fake_run(cmd):
            cmdsrun.append(cmd)
        d = Directory('/foo', commit=False, owner="foo", chmod="0343", 
                      runcmd=fake_run, sudocmd=fake_run)
        d._exists = lambda x: True
        d.run()
        self.assertEqual(['rm /foo', 'mkdir /foo', 'chmod 0343 /foo', 'chown foo /foo'],
                         cmdsrun)

class IDPSymlinkTests(FabricTestCase):
    @server()
    def test_symlink(self):
        s = Symlink('/foo', '/bar', commit=False)
        self.assertEqual(['ln -s /foo /bar'], self.cmdstostr(s.commands))
        s._exists = lambda x: True
        self.assertEqual(['rm /bar', 'ln -s /foo /bar'], self.cmdstostr(s.commands))
        s._is_symlink = lambda x: True
        self.assertEqual(['rm /bar', 'ln -s /foo /bar'], self.cmdstostr(s.commands))
        s._link_points_at_target = lambda: True
        self.assertEqual([], self.cmdstostr(s.commands))
        
        
class IDPGitRepositoryTests(FabricTestCase):
    pass


if __name__=='__main__':
    unittest.main()
