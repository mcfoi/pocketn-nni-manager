"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = pocketn_nni_manager.app:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

from __future__ import annotations
import argparse
from functools import partial
import logging
import os
from pathlib import Path
import sys
from time import sleep
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import PageInfo

from pocketn_nni_manager import __version__, page_login, page_list, page_edit
from pocketn_nni_manager.dbhelper import DbHelper

__author__ = "Marco Foi"
__copyright__ = "Marco Foi"
__license__ = "MIT"

_logger = logging.getLogger("NNIManager")

# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from pocketn_nni_manager.app import fib`,
# when using this Python module as a library.

# ...

# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters
    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).
    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")
    parser.add_argument(
        "--version",
        action="version",
        version=f"pocketn-nni-manager {__version__}",
    )
    parser.add_argument(dest="n", help="n-th Fibonacci number", type=int, metavar="INT")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging
    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s: %(name)s: %(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )

def get_current_page_name():
    ctx = get_script_run_ctx()
    # _logger.info(f"Current context is: {ctx}")
    if ctx is None:
        raise RuntimeError("Couldn't get script context")
    page_name = Path(ctx.main_script_path).stem
    _logger.info(f"Current page name: {page_name}")
    return page_name

def restoreSession():
    dataDir = os.getenv("STREAMLIT_DATA_DIR", "/tmp")
    session_file = f'{dataDir}/session_state.json'
    if (Path(session_file).exists()):
        with open(session_file, 'r') as f:
            import json
            session_data = json.load(f)
            if (session_data != {}):
                _logger.info(f"Session state loaded from {session_file}")
                for key in session_data:
                    st.session_state[key] = session_data[key]
        _logger.info(f"Session state restored from {session_file}")

def saveSession():
    dataDir = os.getenv("STREAMLIT_DATA_DIR", "/tmp")
    session_file = f'{dataDir}/session_state.json'
    with open(session_file, 'w') as f:
        import json
        json.dump(dict(st.session_state), f)
    _logger.info(f"Session state saved to {session_file}")

def deleteSession():
    dataDir = os.getenv("STREAMLIT_DATA_DIR", "/tmp")
    session_file = f'{dataDir}/session_state.json'
    if (Path(session_file).exists()):
        Path(session_file).unlink()
        _logger.info(f"Session state file {session_file} deleted.")

def loginPage():
    st.title('PocketN - NNI Manager')
    st.write("Please log in to continue (username `test`, password `test`).")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if not st.session_state.get("logged_in", False):
        if st.button("Log in", type="primary"):
            if username == "test" and password == "test":
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
                saveSession()
                sleep(0.5)
                st.switch_page(list_varieties_page)
            else:
                st.error("Incorrect username or password")
        else:
            _logger.info(f"Login button not pressed yet.")
    else:
        if st.button("Log out", type="primary"):
            st.session_state.logged_in = False
            st.info("Logged out successfully!")
            _logger.info(f"Logged out successfully!")
            sleep(1.5)
            logout()

def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    _logger.info(f"Logged out successfully!")
    deleteSession()
    sleep(1.5)
    st.switch_page(login_page)



list_varieties_page = st.Page(page_list.listPage, url_path=None, title="Lista Varietà", icon="🌾")
edit_varieties_page = st.Page(page_edit.editPage, url_path=None, title="Modifica Varietà", icon="🌾")
login_page = st.Page(loginPage, title="NNI Manager - Login", icon="🌾", default=True)



def runApp():
    # Setup LOGGING
    setup_logging(logging.INFO)
    # Setup DB
    DbHelper.createDb()

    dataDir = os.getenv("STREAMLIT_DATA_DIR", "/tmp")
    _logger.info(f"DATA DIR is {dataDir}")

    st.set_page_config(layout="wide")
    pages = []
    pg = None

    # Show link to download static file
    # st.markdown("Scarica: [varieties.csv](app/static/varieties.csv)")
    restoreSession()

    with st.sidebar:
        _logger.info(f"Creating Navigation menu")
        if st.session_state.get("logged_in", False):
            _logger.info(f"Utente loggato, mostro sidebar completa.")
            pages.append(list_varieties_page)
            pages.append(edit_varieties_page)
            pg = st.navigation(pages, position="top")
            st.title(" NNI Manager")
            st.subheader("🌾 for PocketN 🌾")
            if st.button("Log out"):
                logout()
        else:
            _logger.info(f"Utente NON loggato: non effettuo la navigazione che bloccherebbe la creazione della pagina di login.")
            pages.append(login_page)
            pg = st.navigation(pages)

    if (pg):
        pg.run()




if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m pocketn_nni_manager.app 42
    #
    # run()
    runApp()
