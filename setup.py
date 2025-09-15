"""Setup script for BagelPay Python SDK"""

from setuptools import setup, find_packages
import os

# Read the README file
here = os.path.abspath(os.path.dirname(__file__)) if '__file__' in globals() else os.getcwd()
try:
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "BagelPay Python SDK - A Python client library for the BagelPay API"

# Read version from __init__.py
def get_version():
    import re
    try:
        with open(os.path.join(here, 'src', 'bagelpay', '__init__.py')) as f:
            content = f.read()
            version_match = re.search(r'^__version__\s*=\s*["\']([^"\']*)["\']', content, re.MULTILINE)
            if version_match:
                return version_match.group(1)
    except FileNotFoundError:
        pass
    return '1.0.0'

__version__ = get_version()

setup(
    name="bagelpay",
    version=__version__,
    author="BagelPay",
    author_email="support@bagelpayment.com",
    description="BagelPay Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bagelpay/bagelpay-sdk-python",
    project_urls={
        "Homepage": "https://bagelpay.io",
        "Bug Reports": "https://github.com/bagelpay/bagelpay-sdk-python/issues",
        "Source": "https://github.com/bagelpay/bagelpay-sdk-python",
        "Documentation": "https://bagelpay.gitbook.io/docs/documentation/sdks/python",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
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
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Office/Business :: Financial :: Point-Of-Sale",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    keywords="bagelpay payment api sdk python",
)