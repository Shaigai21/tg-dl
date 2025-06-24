import glob
from doit.tools import create_folder
from doit.action import CmdAction
import os

HTMLINDEX = "docs/_build/html/index.html"
PODEST = "video_downloader/locales"
POTFILE = "YTIdownl.pot"


def task_html():
    """Gen html docs"""
    all_files = (
        glob.glob("./docs/source/**", recursive=True) +
        glob.glob("./video_downloader/**", recursive=True)
    )
    file_dep = [
        path for path in all_files
        if os.path.isfile(path) and (
            path.endswith(".py") or 
            path.startswith("./docs/source/")
        )
    ]
    return {
        "actions": ['sphinx-build -M html "./docs/source" "docs/_build"'],
        "file_dep": file_dep,
        "targets": [HTMLINDEX],
        "clean": True,
    }


def task_pot():
    """Re-create .pot ."""
    return {
        "actions": [f"pybabel extract -o {POTFILE} YTIdownl"],
        "file_dep": ["video_downloader/__init__.py"],
        "targets": [f"{POTFILE}"],
    }


def task_po():
    """Update locales."""
    return {
        "actions": [
            (create_folder, [f"{PODEST}/ru/LC_MESSAGES"]),
            f"pybabel update --ignore-pot-creation-date -D YTIdownl -d {PODEST} -i {POTFILE}",
        ],
        "file_dep": [f"{POTFILE}"],
        "targets": [f"{PODEST}/ru/LC_MESSAGES/YTIdownl.po"],
    }


def task_mo():
    """Compile locales."""
    return {
        "actions": [
            (create_folder, [f"{PODEST}/ru/LC_MESSAGES"]),
            f"pybabel compile -D tgsaler -l ru -i video_downloader/locales/ru/LC_MESSAGES/YTIdownl.po -d {PODEST}",
        ],
        "file_dep": [f"{PODEST}/ru/LC_MESSAGES/tgsaler.po"],
        "targets": [f"{PODEST}/ru/LC_MESSAGES/tgsaler.mo"],
    }


def task_test():
    """Test programm"""
    return {
        "actions": ["python3 -m unittest -v"],
        "file_dep": [
            f"{PODEST}/ru/LC_MESSAGES/YTIdownl.mo",
            *glob.glob("tgsaler/*.py"),
            "test.py",
        ],
    }


def task_sdist():
    """Initialises project"""
    return {
        "actions": ["python3 -m build --sdist"],
        "targets": ["dist/YTIdownl.tar.gz"],
        "file_dep": [
            "MANIFEST.in",
            "pyproject.toml",
            *glob.glob("./video_downloader/*.py"),
        ],
    }


def task_wheel():
    """Builds wheel"""
    return {
        "actions": ["python3 -m build -n --wheel"],
        "file_dep": [
            "MANIFEST.in",
            "pyproject.toml",
            *glob.glob("./video_downloader/*.py"),
            "dist/YTIdownl-1.0.tar.gz",
        ],
        "verbosity": 0,
    }
