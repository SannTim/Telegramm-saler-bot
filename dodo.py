import glob
from pathlib import Path
import os

HTMLINDEX = "docs/_build/html/index.html"

def task_html():
    """Gen html docs"""
    return {
        "actions": ['sphinx-build -M html "./docs/source" "docs/_build"'],
        "file_dep": [*glob.glob("./docs/source/*"), *glob.glob("./tgsaler/*.py")],
        "targets": [HTMLINDEX],
        "clean": True,
    }
