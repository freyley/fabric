from fabric.contrib.files import exists
from fabric.contrib.files import is_dir
import re
from base import BaseIDP, Command

class File(object):
    pass

class Directory(BaseIDP):
    def __init__(self, name, **kwargs):
        """
        Required Arguments:
           ``name`` the directory path 
        Optional Arguments:
             chmod='0777' to set the permissions. No default.
             user='someuser' to set the user. No default.
             group='somegroup' to set the group. No default.
           `` runcmd``, ``sudocmd``, and ``commit`` from BaseIDP -- see BaseIDP for 
           documentation.

        """
        self.name = name

        self.chmod = self.group = self.user = None
        if 'chmod' in kwargs:
            self.chmod = kwargs.get('chmod')
            if not re.match('^[01234567]{4}$', self.chmod):
                self.chmod = None

        if 'group' in kwargs:
            self.group = kwargs.get('group')
        if 'user' in kwargs:
            self.user = kwargs.get('user')
        super(Directory, self).__init__(**kwargs)
        
    @property
    def commands(self):
        cmds = []
        if self.chmod:
            cmds.append(Command('chmod %s %s' % (self.chmod, self.name)))
        if self.user:
            cmds.append(Command("chown %s %s" % (self.user, self.name), True))
        if self.group:
            cmds.append(Command("chgrp %s %s" % (self.group, self.name), True))
            
        if exists(self.name):
            if is_dir(self.name):
                return cmds
            cmds = [Command('rm %s' % self.name), Command('mkdir %s' % self.name)] + cmds
        cmds = [Command('mkdir -p %s' % self.name) ] + cmds
        return cmds
    
class Symlink(object):
    pass
