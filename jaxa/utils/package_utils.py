import tomlkit


def project_version():
    with open("pyproject.toml") as pyproject:
        file_contents = pyproject.read()

    return str(tomlkit.parse(file_contents)["tool"]["poetry"]["version"])
