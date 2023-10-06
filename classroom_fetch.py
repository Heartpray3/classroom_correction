__author__ = 'Ely Cheikh Abass'
__date__ = '2023-10-05'

from dotenv import load_dotenv
import requests
import json
import os

API_URL = 'https://api.github.com'

load_dotenv()

TOKEN = os.getenv('TOKEN')
CLASSROOM_NAME = os.getenv('CLASSROOM_NAME')
ASSIGNMENT_NAME = os.getenv('ASSIGNMENT_NAME')
OUTPUT_DIR = os.getenv('OUTPUT_DIR')
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28"
}


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


def clone_accepted_assignment(classroom_name: str, assignment_name: str):
    classroom_id = get_classroom_id(classroom_name)
    assignment_id = get_assignment_id(classroom_id, assignment_name)
    accepted_assignments = get(f"{API_URL}/assignments/{assignment_id}/accepted_assignments")
    with open('test.json', 'w') as f:
        json.dump(accepted_assignments, f)
    number_of_repo = 0
    for accepted_assignment in accepted_assignments:
        repo_url = accepted_assignment['repository']['html_url']
        repo_name = accepted_assignment['repository']['full_name']
        clone_cmd = f"git clone {repo_url} {OUTPUT_DIR}/{repo_name}"
        checkout_cmd = f"git checkout -b correction {OUTPUT_DIR}/{repo_name}"
        number_of_repo += 1
        os.system(clone_cmd)
        os.system(checkout_cmd)
        # print(f"Cloned {repo_name} repository of {accepted_assignments['students']}.")
    print(f"Cloned {number_of_repo} from {assignment_name} in the classroom {classroom_name}")


if __name__ == '__main__':

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    try:

        clone_accepted_assignment(CLASSROOM_NAME, ASSIGNMENT_NAME)
        # with open("teams.json", "w") as f:
        #     json.dump(get_organization_teams().json(), f)
    #     # Fetch the list of students and their repositories
    #     response = requests.get(API_URL, headers=headers)
    #     response.raise_for_status()
    #     students = response.json()
    #     print(students)
    #     # for student in students:
    #     #     repo_url = student["repository_url"]
    #     #     repo_name = student["login"]
    #     #     print(student)
    #
    #         # Clone the repository
    #         #

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
