create-python-project
=======================

A script to create an initial project setup. Created out of frustration, when
googling how to import the modules under test to unittest files for the umpth
time.

## Installation

Get the repo from github:

```
git clone https://github.com/tpoikela/create-python-project
```

To create a new project to specified folder, do:
```
bin/create-python-project.py --name project_name --dir project_dir
cd project_dir && make test # Watch tests pass
# Install devdeps
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements_dev.txt
```

Makefile targets:

```
make typecheck
make lint
make coverage
```

## Customisation

Templates are in `tmpl/` folder. Everything is filled up using Python's
`string.Template`. You can customise as you wish.
