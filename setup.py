try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools import find_packages

VERSION = '0.0.2a4'
DESCRIPTION = 'Web-based point of sale system.'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="openwebpos",
    version=VERSION,
    url="https://github.com/baezfb/openwebpos",
    author="Javier Baez",
    author_email="baezdevs@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages('src', exclude=['test*', 'wsgi.py']),
    include_package_data=True,
    package_dir={'': 'src'},
    python_requires='>=3.8',
    homepage="https://github.com/baezfb/OpenWebPOS",
    bugtrack_url="https://github.com/baezfb/OpenWebPOS/issues",
    install_requires=[
        "flask >= 2.0",
        "Flask-SQLAlchemy >= 2.5",
        "Flask-WTF >= 1.0",
        "Flask-Login >= 0.5",
        "python-dotenv >= 0.20"
    ],
    keywords=['python', 'pos', 'point-of-sale'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Framework :: Flask",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "dev": [
            "markdown >= 3.3"
        ]
    },
)
