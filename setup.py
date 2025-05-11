from setuptools import setup, find_packages

# Load the long description from README.md if it exists
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Transmeet is a Python package that transcribes audio files and generates meeting minutes using advanced AI models."

# Load dependencies from requirements.txt
try:
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        requirements = fh.read().splitlines()
except FileNotFoundError:
    requirements = []

setup(
    name="transmeet",
    version="0.0.5",
    author="Deepak Raj",
    author_email="deepak008@live.com",
    description="LLM-powered meeting transcription and summarization tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codeperfectplus/transmeet",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    package_data={
        "transmeet": ["*.conf", "*.ini", "*.json"],
    },
    install_requires=requirements,
    python_requires=">=3.7",
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
    ],
    project_urls={
        "Source": "https://github.com/codeperfectplus/transmeet",
        "Issues": "https://github.com/codeperfectplus/transmeet/issues",
        "Documentation": "https://transmeet.readthedocs.io/en/latest/",
    },
    license="MIT",
)
