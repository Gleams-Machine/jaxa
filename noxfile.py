from nox_poetry import session

# nox.options.sessions = ["static", "unit_tests", "functional_tests"]
PYTHON_VERSIONS = ["3.8", "3.9", "3.10"]


@session(python=PYTHON_VERSIONS)
def with_coverage(session):
    session.install(".")
    session.run(
        "coverage", "run", "-m", "pytest", "tests", "-m", "unit", "-vvs", "-n", "auto"
    )
    session.run("coverage", "report", "-m", "--fail-under", "45")


@session(python=PYTHON_VERSIONS)
def unit_tests(session):
    session.install(".")
    session.run("pytest", "tests", "-m", "unit", "-vvs")  # , "-n", "auto")


@session(python=PYTHON_VERSIONS)
def functional_tests(session):
    session.install(".")
    session.run(
        "pytest", "tests", "-m", "functional", "--json-report-file=functional.json"
    )


@session(python=PYTHON_VERSIONS)
def example_tests(session):
    session.install(".")
    session.run("pytest", "tests", "-m", "example", "--json-report-file=example.json")
