# Release Process

## Preparation

- Update to relevant next version:

```
poetry run prep-dev-release # increase dev version
poetry run prep-patch-release # increase patch version
poetry run prep-minor-release # increase minor version
poetry run prep-major-release # increase major version
```

## Release

```
poetry run release
```

## Configuration

#### For configuring Test PyPI

```
poetry config repositories.test-pypi https://test.pypi.org/legacy/

poetry config pypi-token.test-pypi $TESTPYPI_JAXA_TOKEN

```

#### For configuring PyPI

```
poetry config repositories.pypi https://pypi.org/legacy/

poetry config pypi-token.pypi $PYPI_JAXA_TOKEN

```
