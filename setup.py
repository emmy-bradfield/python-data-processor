from importlib.metadata import entry_points
from setuptools import setup, find_packages

setup(
    name="Ingestion",
    version="0.1.0",
    author="Emily Bradfield",
    author_email="emily-bradfield@outlook.com",
    description="a data ingestion processing tool created from code supplied by cloud academy as part of my training",
    keywords="ingestion data processing",
    url="http://cloudadademy.com",
    packages=find_packages(),
    entry_points={"console_scripts": [
        "ingestiond=ingest.backend:main",
    ]},
    install_requires=[
        "spacy==3.4",
        "spacy-lookups-data==0.3.2",
    ],
    extras_require={
        "dev" : [
            "pytest==5.4.3",
        ]
    }
    
)