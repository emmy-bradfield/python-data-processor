#!/bin/sh

set -e

pip install -e .[dev] 1> /dev/null
pytest ingest/*
python setup.py sdist