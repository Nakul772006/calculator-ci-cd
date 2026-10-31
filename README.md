# Python Calculator CI/CD

A menu-driven command-line calculator project that demonstrates Python development practices and continuous integration with GitHub Actions.

## Project overview

The calculator performs addition, subtraction, multiplication, division, and modulo operations on integer or decimal inputs. It validates menu and number input, and reports zero-divisor errors. Pytest unit tests exercise the calculator functions, while a GitHub Actions workflow compiles the application and runs the test suite on pushes and pull requests.

This repository demonstrates **continuous integration (CI)**. It does not build a production deployment or release pipeline.

## Project objectives

- Build a small, reusable Python command-line application.
- Practice writing focused unit tests with pytest.
- Automate compilation and test execution in GitHub Actions.
- Demonstrate a basic Git and GitHub workflow.

## Features

- Menu-driven interface with an option to exit.
- Addition, subtraction, multiplication, division, and modulo functions.
- Integer and floating-point input support.
- Retry on invalid numeric input.
- Clear handling of division by zero.
- Automated unit tests that do not depend on running the interactive menu.
- CI checks on every push and pull request.

## Technologies

- Python 3.12 (used by the CI workflow)
- pytest
- Git and GitHub
- GitHub Actions

## Project structure

```text
python-calculator-cicd/
├── .github/
│   └── workflows/
│       └── ci.yml
├── tests/
│   └── test_calculator.py
├── .gitignore
├── calculator.py
├── README.md
└── requirements-dev.txt
```

## Prerequisites

- Python 3.12 or later. Python 3.12 is the version configured in CI.
- Git.
- A terminal or command prompt.
- A GitHub account is needed only to publish the repository and use GitHub Actions.

## Installation

Clone the repository, then enter its directory:

```bash
git clone <repository-url>
cd python-calculator-cicd
```

Replace `<repository-url>` with the HTTPS or SSH URL for your GitHub repository. Alternatively, download the repository and open a terminal in its root directory.

## Virtual environment setup

Create a virtual environment in the project directory:

```bash
python -m venv .venv
```

Activate it before installing dependencies or running the application.

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

The `.venv/` directory is excluded from Git by `.gitignore`.

## Install development dependencies

With the virtual environment activated, install pytest:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

## Run the calculator

With the virtual environment activated, launch the application:

```bash
python calculator.py
```

Choose an operation from the menu, enter two numbers when prompted, or choose `5` to exit.

## Run automated tests

Run the test suite from the project root:

```bash
python -m pytest -v
```

The tests cover positive and negative addition, subtraction, multiplication, division, modulo, division by zero, decimal calculations, and retrying after invalid numeric input.

## Git initialization and usage

If you are starting from a project directory that is not already a Git repository, initialize it with the `main` branch:

```bash
git init -b main
```

Stage and commit the project files:

```bash
git add .
git commit -m "Add calculator and CI pipeline"
```

Check the current branch and working tree with:

```bash
git branch --show-current
git status
```

## Set up a GitHub repository

1. Create a new, empty repository on GitHub. If you already have this project locally, avoid initializing the remote with a README or other files to reduce the chance of unrelated history conflicts.
2. Connect the local repository to the GitHub repository. Replace the placeholder with your repository URL:

   ```bash
   git remote add origin <repository-url>
   ```

   If `origin` is already configured, inspect it with `git remote -v` and update it only if it points to the wrong repository.
3. Push the `main` branch:

   ```bash
   git push -u origin main
   ```
4. Open the repository on GitHub and select **Actions** to view workflow runs after a push or pull request triggers the CI workflow.

## GitHub Actions CI pipeline

The workflow is defined in `.github/workflows/ci.yml` and is named **Python Calculator CI**. It triggers on every push and pull request, runs on `ubuntu-latest`, and grants the job read-only `contents` permission.

The job:

1. Checks out the repository with `actions/checkout`.
2. Sets up Python 3.12 with `actions/setup-python`.
3. Upgrades pip and installs `requirements-dev.txt`.
4. Compiles `calculator.py` using `python -m py_compile calculator.py`.
5. Runs the suite using `python -m pytest -v`.

The compile and test commands return a nonzero exit status on failure. GitHub Actions therefore marks the corresponding step and job as failed if compilation or a test fails. The workflow performs CI checks only; it does not deploy the application.

### Example successful workflow

The following is an **illustrative example of expected statuses**, not a report of an actual GitHub Actions run:

```text
Python Calculator CI
└── Compile and test — success
    ├── Check out repository — success
    ├── Set up Python 3.12 — success
    ├── Upgrade pip — success
    ├── Install development dependencies — success
    ├── Compile calculator — success
    └── Run pytest suite — success
```

### Example failed workflow

The following is an **illustrative failure scenario**, not a report of an actual GitHub Actions run. If a test fails, pytest returns a failure status and the job stops with a failed result:

```text
Python Calculator CI
└── Compile and test — failure
    ├── Check out repository — success
    ├── Set up Python 3.12 — success
    ├── Upgrade pip — success
    ├── Install development dependencies — success
    ├── Compile calculator — success
    └── Run pytest suite — failure (one or more tests failed)
```

## Future improvements

- Add linting and formatting checks, such as Ruff.
- Measure test coverage and set a coverage threshold.
- Test against multiple supported Python versions.
- Add tests for additional edge cases, including non-finite numeric values.
- Package the calculator for installation as a command-line tool.
- Add a release workflow if distribution becomes a project goal.
