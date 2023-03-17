from nox_poetry import session

# nox.options.sessions = ["static", "unit_tests", "functional_tests"]
PYTHON_VERSIONS = ["3.8", "3.9", "3.10"]


@session(python=PYTHON_VERSIONS)
def functional_tests(session):
    session.install(".")
    session.run("pytest", "tests", "-m", "functional")


@session(python=PYTHON_VERSIONS)
def jira_issues(session):
    session.install(".")
    session.run("pytest", "tests", "-m", "functional and jira and issues")
