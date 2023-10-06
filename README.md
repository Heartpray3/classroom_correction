# GitHub Classroom Fetcher 🎓

This tool is designed to automate the process of pulling repositories from assignments given in a GitHub classroom based on their names. Not just that, it also checks if the repositories have commits made before a specified deadline. If they do, the script checks out to a new branch named `correction` from that commit. The utility can also push to the appropriate repositories, making the entire correction process smoother.

## Features 🌟

- **Pull Repositories**: Fetch all repositories from an assignment in a GitHub Classroom using their names.
  
- **Commit Check**: Determine if a repository has commits made before a certain deadline.
  
- **Auto Checkout**: If a valid commit is found, checkout to a new branch called `correction` from that commit.
  
- **Push Capability**: Can push the changes back to the appropriate repositories.

## Getting Started 🚀

### Prerequisites

Ensure you have the following:

1. Python installed on your machine.
2. A GitHub Personal Access Token with the necessary permissions.
3. The requirements 

### Setup

1. Clone this repository:

```bash
git clone https://github.com/Heartpray3/classroom_fetch.git
cd classroom_fetch
```

2. Set up the .env file 

In the same directory as [classroom_fetch.py](classroom_fetch.py) create a .env file with the following structure
```
OUTPUT_DIR=your_output_directory
TOKEN=your_github_token
ASSIGNMENT_NAME=name_of_the_assignment
CLASSROOM_NAME=name_of_the_classroom
```

## License 📄

This project is licensed under the MIT License. For more information, see the [LICENSE](LICENSE) file in the repository.

## Support 🙌

If you've found this tool beneficial, please give it a 🌟. For any issues, questions, or suggestions, don't hesitate to open an issue.