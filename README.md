# Python Calculator CI/CD

A command-line and desktop calculator project that demonstrates Python development practices and continuous integration with GitHub Actions.

## Project overview

The calculator provides both a menu-driven command-line interface and a Tkinter desktop interface. Both use the same addition, subtraction, multiplication, division, and modulo functions for integer or decimal inputs. The application validates user input and reports zero-divisor errors. Pytest unit tests exercise the calculator functions, while a GitHub Actions workflow compiles the application and runs the test suite on pushes and pull requests.

This repository demonstrates **continuous integration (CI)**. It does not build a production deployment or release pipeline.

## Project objectives

- Build a small, reusable Python command-line application.
- Practice writing focused unit tests with pytest.
- Automate compilation and test execution in GitHub Actions.
- Demonstrate a basic Git and GitHub workflow.

## Features

- Menu-driven interface with an option to exit.
- Desktop calculator with a keypad, keyboard support, and calculation history display.
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
├── calculator_gui.py
├── README.md
└── requirements-dev.txt
```

## Prerequisites

- Python 3.12 or later. Python 3.12 is the version configured in CI.
- Git.
- A terminal or command prompt.
- A GitHub account is needed only to publish the repository and use GitHub Actions.

The desktop interface also requires Tkinter. It is included with many Python distributions, but may need to be installed separately on Linux. On Ubuntu or Debian, install it before creating the virtual environment:

```bash
sudo apt update
sudo apt install python3-tk
```

On Windows, ensure the Python installation includes **Tcl/Tk support**. On macOS, use a Python distribution that includes Tkinter.

## Installation and setup

Clone the repository, then enter its directory:

```bash
git clone <repository-url>
cd python-calculator-cicd
```

Replace `<repository-url>` with your repository's HTTPS or SSH URL. Alternatively, open a terminal in the project root if you already have the project.

## Virtual environment setup

Create and activate a virtual environment.

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell prevents environment activation, either allow local scripts according to your organization's policy or invoke the environment's Python directly as `.venv\Scripts\python.exe`.

With the virtual environment active, install the development dependencies (pytest):

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

The `.venv/` directory is excluded from Git by `.gitignore`.

## Run the application

### Command-line interface

From the project directory, with the virtual environment active:

```bash
python calculator.py
```

Choose an operation from the menu, enter two numbers when prompted, or choose `6` to exit. If you did not activate the environment, use `.venv/bin/python calculator.py` on Linux/macOS or `.venv\Scripts\python.exe calculator.py` on Windows.

### Desktop interface

With Tkinter installed and a graphical desktop session available, run:

```bash
python calculator_gui.py
```

Use the on-screen keypad or your keyboard to enter calculations. `AC` clears the calculator, `DEL` removes the last digit, and `=` evaluates the expression. Invalid operations are reported in the display. Without activating the environment, use `.venv/bin/python calculator_gui.py` on Linux/macOS or `.venv\Scripts\python.exe calculator_gui.py` on Windows.

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
4. Compiles the command-line and desktop applications using `python -m py_compile calculator.py calculator_gui.py`.
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
