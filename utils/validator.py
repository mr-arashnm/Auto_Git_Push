import os

from os.path import isdir

def validate_repo_path(path):
    """
    Validate if the given path is a valid Git repository.
    """
    if not isdir(path):
        return False
    git_dir = os.path.join(path, '.git')
    return isdir(git_dir)