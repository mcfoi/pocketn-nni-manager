"""
    Setup file for pocketn-nni-manager.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.6.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""

from setuptools import setup

if __name__ == "__main__":
    try:
        setup(use_scm_version={"version_scheme": "no-guess-dev"})
        # To skip using "setuptools-scm", just run:
        # setup()
        # and remove the [tool.setuptools_scm] section of pyproject.toml
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
