# cython: language_level=3
import os
from setuptools import setup, find_packages
from fetch_and_bump_version import get_incremented_version

# ---------------------- Package Metadata ---------------------- #

PACKAGE_NAME = "transmeet"
AUTHOR = "Deepak Raj"
AUTHOR_EMAIL = "deepak008@live.com"
DESCRIPTION = "LLM-powered meeting transcription and summarization tool."
PYTHON_REQUIRES = ">=3.8"
GITHUB_USER = "codeperfectplus"
GITHUB_URL = f"https://github.com/{GITHUB_USER}/{PACKAGE_NAME}"
DOCS_URL = f"https://{PACKAGE_NAME}.readthedocs.io/en/latest/"

# ---------------------- Utility Functions ---------------------- #

def load_file_content(file_path):
    """Read and return the contents of a file if it exists."""
    if os.path.exists(file_path):
        with open(file_path, encoding="utf-8") as f:
            return f.read().strip()
    return ""

def load_requirements(file_path):
    """Parse requirements from a file."""
    content = load_file_content(file_path)
    return content.splitlines() if content else []

# ---------------------- Setup Execution ---------------------- #
setup(
    name=PACKAGE_NAME,
    version=get_incremented_version(PACKAGE_NAME),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=load_file_content("README.md") or DESCRIPTION,
    long_description_content_type="text/markdown",
    url=GITHUB_URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    package_data={
        "transmeet": ["*.conf", "*.ini", "*.json", "prompts/*"]
    },
    install_requires= load_requirements("requirements.txt"),
    python_requires= PYTHON_REQUIRES,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
    ],
    entry_points={
        "console_scripts": [
            "transmeet=transmeet.cli:main",
        ],
    },
    keywords=[
        "transcription",
        "meeting summarization",
        "audio processing",
        "LLM",
        "Groq",
        "Google Speech",
        "CLI",
        "automation",
        "speak2summary"
    ],
    project_urls={
        "Source": "https://github.com/codeperfectplus/transmeet",
        "Issues": "https://github.com/codeperfectplus/transmeet/issues",
        "Documentation": "https://transmeet.readthedocs.io/en/latest/",
    },
    license="MIT",
)
