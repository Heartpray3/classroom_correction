__author__ = 'Ely Cheikh Abass'
__date__ = '2023-10-05'

import os
import subprocess
from dotenv import load_dotenv
from variables import *


def find_git_repos():
    git_repos = []
    for dir_path, dir_names, filenames in os.walk(os.environ['OUTPUT_DIR']):
        if ".git" in dir_names:
            git_repos.append(dir_path)
    return git_repos


def commit_and_push_git_repo(directory):
    """Commits and pushes the Git repository in the given directory."""
    curr_dir = os.getcwd()
    try:
        os.chdir(directory)
        # Add all changes to the staging area
        subprocess.run(["git", "add", "-A"], check=True)

        # Commit the changes
        commit_msg = 'Automatic commit : correction'
        result = subprocess.run(['git', 'commit', '-m', commit_msg], capture_output=True, text=True)
        if result.returncode not in (0, 1):  # Code 1 means nothing to commit
            raise NotADirectoryError(f"Failed to commit in {directory}. Error: {result.stderr}")
        elif result.returncode == 1:
            print(f"{END_L}{OFFSET}\n{RED}Nothing to commit in {directory}{RESET}\n{OFFSET}{END_L}")
            return

        # Push the changes
        result = subprocess.run(["git", "push"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Pushed repository at {directory}")
        else:
            raise NotADirectoryError(f"Failed to push repository at {directory}. Error: {result.stderr}")

    except NotADirectoryError as e:
        print(f"Error while commit/push : {e}")
    except subprocess.CalledProcessError:
        print(f"Error processing {directory}.")
    finally:
        os.chdir(curr_dir)


if __name__ == '__main__':
    load_dotenv(dotenv_path='.env')
    # classroom_id = get_classroom_id(lo)
    find_git_repos()
