from base import BaseIDP, Command
from fs import Directory
from fabric.contrib.files import is_dir, exists
from os.path import join, basename, dirname
import copy
from fabric.state import env

class GitRepository(BaseIDP):
    def __init__(self, repo_path, repo_remote, **kwargs):
        """ 
        Ensure a Git repository is in the specified place and is up-to-date.
        Uses ssh-agent to clone and pull the repo.
        Arguments:
            `` repo_path`` : location or Directory location of repo. If not a Directory,
            **kwargs will be passed to Directory for creation, so you can pass chmod, 
            owner, and group
            `` repo_remote``: remote repo url to pass to git for clone
         Optional Arguments:
           `` runcmd``, ``sudocmd``, and ``commit`` from BaseIDP -- see BaseIDP for 
           documentation.
        """

        self.repo_path = repo_path
        self.repo_parent_dir = dirname(self.repo_path)
        self.repo_directory_name = basename(self.repo_path)
        kwargs_no_commit = copy.deepcopy(kwargs)
        if 'commit' in kwargs_no_commit:
            del kwargs_no_commit['commit']
        if type(self.repo_path) != Directory:
            self.repo_path = Directory(self.repo_path, commit=False, **kwargs_no_commit)
        self.repo_remote = repo_remote
        super(GitRepository, self).__init__(**kwargs)

    @property
    def commands(self):
        cmds = []
        if is_dir(self.repo_path.path) and not is_dir(join(self.repo_path.path, '.git')):
            cmds.append(Command('rm -r %s' % self.repo_path.path))
        if not is_dir(join(self.repo_path.path, '.git')):
            cmds.append(self._clone_command)
        elif not exists(join(self.repo_path.path, '.git', 'config')):
            # TODO: what do I do here?
            pass
        else:
            # determine if config points to the right place
            cmds.append(self._pull_command)
        return cmds

    @property
    def _clone_command(self):
        clone_cmd = 'cd %s; git clone %s %s' % (self.repo_parent_dir, 
                                                self.repo_remote, self.repo_directory_name)
        return Command("ssh -A %s '%s'" % (env.host_string, clone_cmd), run_local=True)

    @property
    def _pull_command(self):
        pull_cmd = 'cd %s; git pull' % self.repo_path.path
        return Command("ssh -A %s '%s'" % (env.host_string, pull_cmd), run_local=True)

