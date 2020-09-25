#!/usr/bin/env bash
mkdir -p reports
tox
pip install pylint
pylint -r y -s y -f json --exit-zero src/ --exit-zero > reports/pylint.json

