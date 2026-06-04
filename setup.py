#!/usr/bin/env python3
"""
TokenSqueeze - Setup script
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tokensqueeze",
    version="1.0.0",
    author="TokenSqueeze Team",
    author_email="tokensqueeze@example.com",
    description="Lightweight LLM Input Intelligent Compression Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/TokenSqueeze-CLI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "tokensqueeze=tokensqueeze.cli:main",
            "tokensqueeze-tui=tokensqueeze.tui:main",
        ],
    },
    keywords="llm token compression cli tool ai",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/TokenSqueeze-CLI/issues",
        "Source": "https://github.com/gitstq/TokenSqueeze-CLI",
    },
)
