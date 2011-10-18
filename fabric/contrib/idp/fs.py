from fabric.contrib.files import exists
from fabric.contrib.files import is_dir
import re
from .base import BaseIDP, Command

class File(object):
    pass

class Directory(BaseIDP):
    def __init__(self, name, **kwargs):
        """
        Required Arguments:
           ``name`` the directory path 
        Optional Arguments:
             chmod='0777' to set the permissions. No default.
             owner='someuser' to set the owner. No default.
             group='somegroup' to set the group. No default.
           `` runcmd``, ``sudocmd``, and ``commit`` from BaseIDP -- see BaseIDP for 
           documentation.

        """
        self.name = name

        self.chmod = self.group = self.owner = None
        if 'chmod' in kwargs:
            self.chmod = kwargs.get('chmod')
            if not re.match('^[01234567]{4}$', self.chmod):
                self.chmod = None

        if 'group' in kwargs:
            self.group = kwargs.get('group')
        if 'owner' in kwargs:
            self.owner = kwargs.get('owner')
        super(Directory, self).__init__(**kwargs)
        self._exists = exists
        self._is_dir = is_dir

    @property
    def commands(self):
        cmds = []
        if self.chmod:
            cmds.append(Command('chmod %s %s' % (self.chmod, self.name)))
        if self.owner:
            cmds.append(Command("chown %s %s" % (self.owner, self.name), True))
        if self.group:
            cmds.append(Command("chgrp %s %s" % (self.group, self.name), True))
            
        if self._exists(self.name):
            if self._is_dir(self.name):
                return cmds
            else:
                cmds = [Command('rm %s' % self.name), Command('mkdir %s' % self.name)] + cmds
        else:
            cmds = [Command('mkdir -p %s' % self.name) ] + cmds
        return cmds
    
class Symlink(object):
    pass
