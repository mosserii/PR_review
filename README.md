# PR Review with OpenAI
This tool aims to enhance the code review process by providing valuable comments and suggestions for changes. By offering automated and intelligent feedback, it seeks to improve code quality and accelerate development cycles.

### Prerequisites

Before using this code, make sure you have the following:

- OpenAI API key: You need an API key to interact with OpenAI's language model. If you don't have one, sign up here : https://platform.openai.com/api-keys.
- GitHub repository: You should have a GitHub repository where you want to enable code reviews. Ensure that you have the necessary permissions to add workflows and access pull requests.

### Usage

To enable code review with OpenAI on your GitHub repository, follow these steps:

1. Fork this repository: Click the "Fork" button at the top-right corner of this repository to create a copy of it in your own GitHub account.
2. Get the OpenAI API key: Sign up for OpenAI and obtain an API key that allows you to interact with OpenAI's language model.
3. Add the API key as a secret: In your forked repository, go to the "Settings" tab and click on "Secrets" in the left sidebar. Add a new secret called `OPENAI_API_KEY` and paste your OpenAI API key as the value, do the same with `MY_GITHUB_TOKEN`.
4. Create a workflow file: In your forked repository, navigate to the `.github/workflows/` directory and create a new file called `code_review.yml`. Copy and paste the 
code_review.yml content.
5. Commit and push the changes: Commit the new workflow file (`code_review.yml`) to your forked repository and push the changes to GitHub. That's it! The code review workflow is now set up on your GitHub repository. Whenever a pull request is opened or updated, the workflow will automatically execute and post the code review as a comment on the pull request.



## Example : 

for the code :

file1.py:
```python
def hello():
    print('Hello, world!')
```

file2.py:
```python
def add(a, b):
    return a + b
```


This comment will be added: 

Here are my feedback and change suggestions for the code changes in the PR:

File: file1.py
- The function `hello` should have a docstring to describe what it does.
- You could consider adding a return statement to the function `hello` so that it returns a value.

Here's an updated version of `file1.py` with the suggested changes:
```python
def hello():
    
    Prints 'Hello, world!' to the console.
    
    print('Hello, world!')
    return  # optional, if you don't need to return anything
```

File: file2.py
- The function `add` should have a docstring to describe what it does.
- You could consider adding type hints for the function arguments and return type to improve readability and maintainability.

Here's an updated version of `file2.py` with the suggested changes:
```python
def add(a: int, b: int) -> int:
    
    Returns the sum of two numbers, a and b.
    
    Args:
        a (int): First number.
        b (int): Second number.
    
    Returns:
        int: The sum of a and b.
    
    return a + b
```

These changes will help enhance the readability, maintainability, and documentation of the code

