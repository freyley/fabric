from fabric.contrib.files import exists
from fabric.contrib.files import is_dir, is_symlink
import re
from .base import BaseIDP, Command

class PermissionsBase(BaseIDP):
    def __init__(self, **kwargs):
        """
        Optional Arguments:
             chmod='0777' to set the permissions. No default.
             owner='someuser' to set the owner. No default.
             group='somegroup' to set the group. No default.
        """
        self.chmod = self.group = self.owner = None
        if 'chmod' in kwargs:
            self.chmod = kwargs.get('chmod')
            if not re.match('^[01234567]{4}$', self.chmod):
                self.chmod = None

        if 'group' in kwargs:
            self.group = kwargs.get('group')
        if 'owner' in kwargs:
            self.owner = kwargs.get('owner')
        self._exists = exists
        self._is_dir = is_dir
        self._is_symlink = is_symlink
        super(PermissionsBase, self).__init__(**kwargs)

    @property
    def commands(self):
        cmds = []
        if self.chmod:
            cmds.append(Command('chmod %s %s' % (self.chmod, self.name)))
        if self.owner:
            cmds.append(Command("chown %s %s" % (self.owner, self.name), True))
        if self.group:
            cmds.append(Command("chgrp %s %s" % (self.group, self.name), True))
        return cmds

class Directory(PermissionsBase):
    def __init__(self, name, **kwargs):
        """
        Required Arguments:
           ``name`` the directory path 
        Optional Arguments:
          ``chmod``, ``group``, and ``owner`` from PermissionsBase, see it documentation.
           `` runcmd``, ``sudocmd``, and ``commit`` from BaseIDP -- see it for 
           documentation.

        """
        self.name = name

        super(Directory, self).__init__(**kwargs)

    @property
    def commands(self):
        cmds = super(Directory,self).commands
        if self._exists(self.name):
            if self._is_dir(self.name):
                return cmds
            else:
                cmds = [Command('rm %s' % self.name), Command('mkdir %s' % self.name)] + cmds
        else:
            cmds = [Command('mkdir -p %s' % self.name) ] + cmds
        return cmds
    
class Symlink(PermissionsBase):
    def __init__(self, target, link_name, **kwargs):
        """
        Required Arguments:
           ``target`` the target path
           ``link_name`` the link itself
        Optional Arguments:
          ``chmod``, ``group``, and ``owner`` from PermissionsBase, see it documentation.
           `` runcmd``, ``sudocmd``, and ``commit`` from BaseIDP -- see it for 
           documentation.

        """
        self.target = target
        self.link_name = link_name
        super(Symlink, self).__init__(**kwargs)

    def _link_points_at_target(self):
        """a better implementation would reduce commands needed to ensure where the link points"""
        return False

    @property
    def make_link_cmd(self):
        return Command('ln -s %s %s' % (self.target, self.link_name))
    @property
    def remove_link_cmd(self):
        return Command('rm %s' % self.link_name, True)
    @property
    def commands(self):
        cmds = super(Symlink,self).commands
        if self._exists(self.link_name):
            if self._is_symlink(self.link_name):
                if self._link_points_at_target():
                    return cmds
                else:
                    return [self.remove_link_cmd, self.make_link_cmd ] + cmds
            else:
                return [self.remove_link_cmd, self.make_link_cmd ] + cmds
        else:
            return [self.make_link_cmd] + cmds

