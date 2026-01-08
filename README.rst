.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/pocketn-nni-manager.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/pocketn-nni-manager
    .. image:: https://readthedocs.org/projects/pocketn-nni-manager/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://pocketn-nni-manager.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/pocketn-nni-manager/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/pocketn-nni-manager
    .. image:: https://img.shields.io/pypi/v/pocketn-nni-manager.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/pocketn-nni-manager/
    .. image:: https://img.shields.io/conda/vn/conda-forge/pocketn-nni-manager.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/pocketn-nni-manager
    .. image:: https://pepy.tech/badge/pocketn-nni-manager/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/pocketn-nni-manager
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/pocketn-nni-manager

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

===================
pocketn-nni-manager
===================


    Package containing the Streamlit application to NNI Manager!


This package was created using the following list of commands:

$ pip install pyscaffold
$ putup -i pocketn-nni-manager
$ cd pocketn-nni-manager
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -U pip setuptools setuptools_scm build tox
# ... edit setup.cfg to add dependencies ...

# To define a VERSION before building => set a Git TAG (git is REQUIRED) that will be used by 'setuptools-scm':
# [https://pyscaffold.org/en/stable/faq.html]
$ git tag v1.2.3

# To install an EDITABLE version during DEVELOPMENT (this will also install all requirements from section 'install_requires' of `setup.cfg``):
$ pip install -e .
$ tox

# To build a .whl for distribution:
$ tox -e build
# or (does not crete sbuild)
$ python -m build --wheel


A longer description of your project goes here...


DOCKER

Image can be created
- once .whl file has been built (so is available in `dist` folder)
- `Dockerfile` has been updated to copy the .whl file in the image (always done as whole `dist` is copied)
- and `requirements.txt` installs it <= CHANGE VERSION NUMBER HERE TO MATCH GIT TAG>

```docker build . -t cassandratech/pocketn-nni-manager:1.0.6 -t cassandratech/pocketn-nni-manager:latest```

The created image can be run locally using:<br/>

```docker run --rm --name pocketn-nni-manager -p 8501:8501 cassandratech/pocketn-nni-manager:latest```

.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.6. For details and usage
information on PyScaffold see https://pyscaffold.org/.
