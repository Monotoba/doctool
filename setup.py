#!/usr/bin/env python3
"""
Setup script for the document conversion tool.
"""

from setuptools import setup, find_packages

setup(
    name="docconvert",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "markdown>=3.3.0",
        "weasyprint>=52.5",
        "PyPDF2>=2.0.0",
        "pyyaml>=6.0",
        "html2text>=2020.1.16",
        "odfpy>=1.4.1",
        "Pillow>=9.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.1.0",
            "flake8>=4.0.1",
            "mypy>=0.931",
        ],
    },
    python_requires=">=3.8",
)