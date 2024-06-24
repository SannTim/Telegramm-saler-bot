import glob
from pathlib import Path
from doit.tools import create_folder
import os

HTMLINDEX = "docs/_build/html/index.html"
PODEST = "tgsaler/translations"
POTFILE = "tgsaler.pot"

def task_html():
    """Gen html docs"""
    return {
        "actions": ['sphinx-build -M html "./docs/source" "docs/_build"'],
        "file_dep": [*glob.glob("./docs/source/*"), *glob.glob("./tgsaler/*.py")],
        "targets": [HTMLINDEX],
        "clean": True,
    }

def task_pot():
    """Re-create .pot ."""
    return {
        "actions": [f"pybabel extract -o {POTFILE} tgsaler"],
        "file_dep": ["tgsaler/bd_console/__init__.py"],
        "targets": [f"{POTFILE}"],
    }


def task_po():
    """Update translations."""
    return {
        "actions": [
            (create_folder, [f"{PODEST}/ru/LC_MESSAGES"]),
            f"pybabel update --ignore-pot-creation-date -D tgsaler -d {PODEST} -i {POTFILE}"
        ],
        "file_dep": [f"{POTFILE}"],
        "targets": [f"{PODEST}/ru/LC_MESSAGES/tgsaler.po"],
    }


def task_mo():
    """Compile translations."""
    return {
        "actions": [
            (create_folder, [f"{PODEST}/ru/LC_MESSAGES"]),
            f"pybabel compile -D tgsaler -l ru -i tgsaler/translations/ru/LC_MESSAGES/tgsaler.po -d {PODEST}",
        ],
        "file_dep": [f"{PODEST}/ru/LC_MESSAGES/tgsaler.po"],
        "targets": [f"{PODEST}/ru/LC_MESSAGES/tgsaler.mo"],
    }

def task_test():
    """Test programm"""
    return {
        "actions": ["python3 -m unittest -v"],
        "file_dep": [
            f"{PODEST}/ru/LC_MESSAGES/tgsaler.mo",
            *glob.glob("tgsaler/*.py"),
            "test.py"
        ],
    }

def task_sdist():
    """Initialises project"""
    return {
        "actions": ["python3 -m build --sdist"],
        "targets": ["dist/tgsaler-1.0.tar.gz"],
        "file_dep": [
            "MANIFEST.in",
            "pyproject.toml",
            *glob.glob("./tgsaler/*.py"),
        ],
    }


def task_wheel():
    """Builds wheel"""
    return {
        "actions": ["python3 -m build -n --wheel"],
        "file_dep": [
            "MANIFEST.in",
            "pyproject.toml",
            *glob.glob("./tgsaler/*.py"),
            "dist/tgsaler-1.0.tar.gz",
        ],
        "verbosity": 0,
    }
