from fabric.api import sudo, run
from fabric.api import local as run_local

class Command(object):
    def __init__(self, cmd, use_sudo=False, run_local=False):
        self.cmd = cmd
        self.use_sudo = use_sudo
        self.run_local=run_local

    def __unicode__(self):
        return self.cmd

class BaseIDP(object):
    def __init__(self, **kwargs):
        """   
          ``runcmd`` sets the command to use when running actions. 
                             default: fabric.api.run
          ``sudocmd`` sets the command to use when running chgrp and chown. 
                               default: fabric.api.sudo
          ``localcmd`` sets the command to use when running local commands.
                               local commands are used primarily when something needs ssh key forwarding
                               default: fabric.api.local
          ``commit`` False prevents immediate action, can call run() after. default: True
        """

        if 'runcmd' in kwargs and callable(kwargs.get('runcmd')):
            self.runcmd = kwargs.get('runcmd')
        else:
            self.runcmd = run
        if 'sudocmd' in kwargs and callable(kwargs.get('sudocmd')):
            self.sudocmd = kwargs.get('sudocmd')
        else:
            self.sudocmd = sudo
        if 'localcmd' in kwargs and callable(kwargs.get('localcmd')):
            self.localcmd = kwargs.get('localcmd')
        else:
            self.localcmd = run_local

        if 'commit' in kwargs and kwargs.get('commit'):
            self.run(self.commands)

    def run(self, *args):
        commands = args
        if not commands:
            commands = self.commands
        for c in commands:
            if c.use_sudo:
                self.sudocmd(unicode(c))
            elif c.run_local:
                self.localcmd(unicode(c))
            else:
                self.runcmd(unicode(c))
                
    @property
    def commands(self):
        raise NotImplementedError("run not implemented.")

                                 
