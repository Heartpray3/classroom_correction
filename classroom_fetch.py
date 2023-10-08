__author__ = 'Ely Cheikh Abass'
__date__ = '2023-10-05'

from dotenv import load_dotenv
import subprocess
import requests
import json
import os
import re
import base64

RED = '\033[91m'
RESET = '\033[0m'
END_L = '\n' * 3
OFFSET = 50 * '*'

API_URL = 'https://api.github.com'


def get(path: str):
    response = requests.get(path, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def find_key(response_list, key_term, name):
    ind = next((index for index, response in enumerate(response_list) if response[key_term] == name), -1)
    if ind == -1:
        raise NameError(f"The {key_term} {name} is not found")
    return response_list[ind]['id']


def get_classroom_id(classroom_name: str):
    classrooms = get(f"{API_URL}/classrooms")
    return find_key(classrooms, 'name', classroom_name)


def get_assignment_id(classroom_id: int, assignment_name: str):
    assignments = get(f"{API_URL}/classrooms/{classroom_id}/assignments")
    return find_key(assignments, 'title', assignment_name)


def write_readme_correction():
    content = get(f"{API_URL}/repos/{TEMPLATE_REPO}/contents/{PATH_DESCRIPTION}")

    content = base64.b64decode(content['content']).decode('utf-8')

    # Step 2: Use a regular expression to extract the desired content
    # The regular expression captures content starting from "## Barème de correction" to the next "##"
    match = re.search(r'(## Barème de correction.*?)(?=##|$)', content, re.DOTALL)

    if match:
        extracted_content = match.group(1)
    else:
        raise KeyError("Section not found!")

    extracted_content = re.sub(r'(?<=\| )(\d+)(?=\s*(\n|$))', r'note/\1', extracted_content)

    # Step 3: Write the extracted content to a file in the desired repository
    output_file_path = 'correction.md'
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(extracted_content)


def clone_accepted_assignment(classroom_name: str, assignment_name: str):
    classroom_id = get_classroom_id(classroom_name)
    assignment_id = get_assignment_id(classroom_id, assignment_name)
    accepted_assignments = get(f"{API_URL}/assignments/{assignment_id}/accepted_assignments")
    deadline = get(f"{API_URL}/assignments/{assignment_id}")['deadline']
    number_of_repo = 0

    for accepted_assignment in accepted_assignments:
        repo_url = accepted_assignment['repository']['html_url']
        repo_name = accepted_assignment['repository']['full_name']
        repo_name = os.path.split(repo_name)[1]
        clone_cmd = f"git clone {repo_url} {repo_name}"
        number_of_repo += 1
        os.chdir(PATH)
        os.chdir(OUTPUT_DIR)
        os.system(clone_cmd)

        # Find the latest commit before the deadline
        os.chdir(os.path.join(OUTPUT_DIR, repo_name))
        find_commit_cmd = f"git rev-list -1 --before='{deadline}' main"
        result = os.popen(find_commit_cmd).read().strip()
        if result:  # Check if there is a commit hash returned
            checkout_cmd = f"git checkout -b correction {result}"
            os.system(checkout_cmd)
            write_readme_correction()
        else:
            print(f"{END_L}{OFFSET}\n{RED}No commit found before deadline for repo {repo_name}{RESET}\n{OFFSET}{END_L}")

    print(f"Cloned {number_of_repo} from {assignment_name} in the classroom {classroom_name}")


if __name__ == '__main__':
    load_dotenv()

    TOKEN = os.getenv('TOKEN')
    CLASSROOM_NAME = os.getenv('CLASSROOM_NAME')
    ASSIGNMENT_NAME = os.getenv('ASSIGNMENT_NAME')
    OUTPUT_DIR = os.getenv('OUTPUT_DIR')
    TEMPLATE_REPO = os.getenv('TEMPLATE_REPO')
    PATH_DESCRIPTION = os.getenv('PATH_DESCRIPTION')
    HEADERS = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    PATH = os.getcwd()
    try:
        clone_accepted_assignment(CLASSROOM_NAME, ASSIGNMENT_NAME)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
