#!/bin/bash

path=$1

echo "running black"
poetry run black "$path"

echo "running isort"
poetry run isort --profile black "$path"

echo "running flake8"
poetry run flake8 "$path"

echo "running mypy"
poetry run mypy "$path"
