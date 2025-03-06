from setuptools import setup, find_packages

setup(
    name="imap_to_mongo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pymongo>=4.0.0",
        "imaplib2>=3.6",
        "dnspython>=2.0.0",
    ],
    author="OpenHands",
    author_email="openhands@all-hands.dev",
    description="A package to fetch emails from IMAP server and store them in MongoDB",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)