from base import BaseIDP
from fs import Directory
from fabric.contrib.files import is_dir, exists
from os.path import join

class GitRepository(BaseIDP):
    def __init__(self, repo_path, repo_remote, **kwargs):
        """ 
        Ensure a Git repository is in the specified place and is up-to-date.
        Uses ssh-agent to clone and pull the repo.
        Arguments:
            `` repo_path`` : location or Directory location of repo. If not a Directory,
            **kwargs will be passed to Directory for creation, so you can pass chmod, 
            user, and group
            `` repo_remote``: remote repo url to pass to git for clone
         Optional Arguments:
           `` runcmd``, ``sudocmd``, and ``commit`` from BaseIDP -- see BaseIDP for 
           documentation.
        """

        self.repo_path = repo_path
        if type(self.repo_path) != Directory:
            self.repo_path = Directory(self.repo_path, commit=False, **kwargs)
        self.repo_remote = repo_remote
        super(GitRepository, self).__init__(**kwargs)

    @property
    def commands(self):
        cmds = []
        if not is_dir(self.repo_path.path):
            cmds.append(self._clone_command)
        elif not is_dir(join(self.repo_path.path, '.git')):
            # TODO: what do I do here?
            pass
        elif not exists(join(self.repo_path.path, '.git', 'config')):
            # TODO: what do I do here?
            pass
        else:
            # determine if config points to the right place
            cmds.append(self._pull_command)
    @property
    def _clone_command(self):
        pass

    @property
    def _pull_command(self):
        pass

