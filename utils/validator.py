import os

def validate_repo_path(path):
    """
    Validate if the given path is a valid Git repository.

    :param path: The path to validate.
    :return: True if the path is a valid Git repository, False otherwise.
    """
    git_dir = os.path.join(path, ".git")
    return os.path.isdir(git_dir)