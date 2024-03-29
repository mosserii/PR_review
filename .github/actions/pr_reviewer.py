import json
import os
import textwrap
import openai
from github import Github
from github.PullRequest import PullRequest
from openai import OpenAI
import git

TOKEN_LIMIT = 4095


def get_file_content(file_path: str) -> str:
    """
    reads the content of file at file_path
    :param file_path: the file to get content from
    :return: the content of the file
    """
    with open(file_path, 'r') as file:
        return file.read()


def get_changed_files(pr: PullRequest) -> dict:
    """
    check which files were changed in the pull request and adds them to the changed_files dict
    :param pr: the pull request object
    :return:  dict with key : file path, value : file content
    """
    # Clone the repository and "checkout" the PR branch
    repo = git.Repo.clone_from(pr.base.repo.clone_url, to_path='./repo', branch=pr.head.ref)

    # Get the difference between the PR branch and the base branch
    base_ref = f"origin/{pr.base.ref}"
    head_ref = f"origin/{pr.head.ref}"
    diffs = repo.git.diff(base_ref, head_ref, name_only=True).split('\n')

    # changed_files (key : file path, value : file content) - only files that were changed
    changed_files = {}
    for file_path in diffs:
        try:
            # Fetch each file's content and store it in the changed_files dictionary
            changed_files[file_path] = get_file_content('./repo/' + file_path)
        except Exception as e:
            print(f"Failed to read {file_path}: {e}")

    return changed_files


def send_to_openai(files: dict) -> str:
    """
    send to openai all the files that were changed and getting back a review
    :param files: the files that were changed in the pull request
    :return: review from openAI
    """

    # Concatenate all the files into a single string with 2 empty lines between each file
    code = ""
    for file_name, file_content in files.items():
        code += f"File: {file_name}\n{file_content}\n\n"

    # Split the code into chunks that are each within the token limit
    chunks = textwrap.wrap(code, TOKEN_LIMIT)
    my_api_key = os.getenv('OPENAI_API_KEY')

    client = OpenAI(
        api_key=my_api_key,
    )

    reviews = []
    for chunk in chunks:
        # Send a message to OpenAI with each chunk of the code for review
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are analyzing a GitHub PR. Please provide feedback and change suggestions for the code changes.",
                },
                {
                    "role": "user",
                    "content": "Here are the code changes in the PR:\n" + chunk,
                },
            ],
        )
        # Add the assistant's reply to the list of reviews
        reviews.append(response.choices[0].message.content)

    # Join all the reviews into a single string
    review = "\n".join(reviews)

    return review


def post_comment_on_pr(pr: PullRequest, comment: str):
    """
    posts a comment on the pull request
    :param pr: pull request
    :param comment: the comment that came back from openai
    """
    # Post the OpenAI's response as a comment on the PR
    pr.create_issue_comment(comment)


def main():
    try:
        github_token = os.getenv('MY_GITHUB_TOKEN')
        g = Github(github_token)
        # Get the pull request JSON
        with open(os.getenv('GITHUB_EVENT_PATH')) as json_file:
            event = json.load(json_file)

        # Get the pull request object
        repository = g.get_repo(event['repository']['full_name'])
        pr_number = event['pull_request']['number']
        pr = repository.get_pull(pr_number)
        # Get the changed files in the pull request
        files = get_changed_files(pr)
        # Send the files to OpenAI for review
        review = send_to_openai(files)
        # Post the review as a comment on the pull request
        pr.create_issue_comment(review)

    except openai.RateLimitError:
        print("Rate limit exceeded. Please try again later.")
    except openai.OpenAIError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

