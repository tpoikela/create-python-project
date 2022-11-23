create-python-project
=======================

A script to create an initial Python project setup. Created out of frustration, when
googling how to import the modules under test to unittest files for the umpth
time.

Features:
Creates README.md, src and test folders, Makefile, .gitignore, LICENSE, VERSION
and setup.py.

## Installation

Get the repo from github:

```
git clone https://github.com/tpoikela/create-python-project
```

To create a new project to specified folder, do:
```
bin/create-python-project.py create --name project_name --dir project_dir mod1 mod2
cd project_dir && make test # Watch tests pass
# Install devdeps
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements_dev.txt
```

The following files/directories are generated:

```
./project_dir/
├── LICENSE
├── Makefile
├── README.md
├── requirements_dev.txt
├── setup.py
├── src
│   ├── __init__.py
│   ├── mod1.py
│   └── mod2.py
├── test
│   ├── __init__.py
│   ├── test_mod1.py
│   └── test_mod2.py
└── VERSION
```

2 directories, 12 files

Makefile targets:

```
make typecheck
make lint
make coverage
```

## Customisation

Templates are in `tmpl/` folder. Everything is filled up using Python's
`string.Template`. You can customise as you wish.

You can add variables to templates using `$varname`. To fill the value in
template, use the `--data` argument:

```
bin/create-python-project.py create ... --data varname=value var2=val2 -- files
```
