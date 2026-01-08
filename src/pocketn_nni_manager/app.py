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
import logging
from pathlib import Path
import sys
from time import sleep
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import PageInfo

from pocketn_nni_manager import __version__, page_login, page_list, page_edit

__author__ = "Marco Foi"
__copyright__ = "Marco Foi"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from pocketn_nni_manager.app import fib`,
# when using this Python module as a library.


def fib(n):
    """Fibonacci example function

    Args:
      n (int): integer

    Returns:
      int: n-th Fibonacci number
    """
    assert n > 0
    a, b = 1, 1
    for _i in range(n - 1):
        a, b = b, a + b
    return a


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
    logformat = "[%(asctime)s] %(levelname)s:%(name)s: %(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting crazy calculations...")
    print(f"The {args.n}-th Fibonacci number is {fib(args.n)}")
    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


# app_page = st.Page("app.py", title="NNI Manager - Login", icon="🌾", default=True)

def runApp():
    """ Calls :func:`mainApp`"""
    mainApp()

def get_current_page_name():
    ctx = get_script_run_ctx()
    # _logger.info(f"Current context is: {ctx}")
    if ctx is None:
        raise RuntimeError("Couldn't get script context")
    page_name = Path(ctx.main_script_path).stem
    _logger.info(f"Current page name: {page_name}")
    return page_name

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

# def listPage():
#     # List page content
#     st.markdown("## Lista varietà 🎈")
#     # st.sidebar.markdown("# Pagina varietà🎈")

# def editPage():
#     # Main page content
#     st.markdown("## Modifica varietà 🎈")
#     # st.sidebar.markdown("# Pagina varietà🎈")

def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    _logger.info(f"Logged out successfully!")
    sleep(1.5)
    st.switch_page(login_page)

list_varieties_page = st.Page(page_list.listPage, title="Lista Varietà", icon="🌾")
edit_varieties_page = st.Page(page_edit.editPage, title="Modifica Varietà", icon="🌾")
# login_page = st.Page("page_login.py", title="Login Page", icon="💎", default=True)
login_page = st.Page(loginPage, title="NNI Manager - Login", icon="🌾", default=True)

def mainApp():
    setup_logging(logging.INFO)

    pages = []
    pg = None

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
