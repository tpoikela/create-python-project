#! /usr/bin/env python3

"""
create-python-project is a command suite for creating new Python project. 

Following commands are supported:
  - create: Creates a new project. Supports following arguments:
    * --name: Name of the new project
    * --dir:  Directory of the new project
    * --force: Overwrites existing project
    * --files: Python files to create in src folder and test folder
    * --data: Key-value pairs used in templates.

"""

import argparse
import os
from string import Template
import urllib.request

MIT_LIC_URL = 'https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/_licenses/mit.txt'
GIT_IGN_URL = 'https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore'

def create_arg_parser():
    """ Creates new argparser supporting specified commands and arguments """
    parser = argparse.ArgumentParser(description='create-python-project is a command suite for creating new Python project.')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    create_parser = subparsers.add_parser('create', help='Creates a new project')
    create_parser.add_argument('--name', help='Name of the new project', required=True)
    create_parser.add_argument('--dir', help='Directory of the new project', required=True)
    create_parser.add_argument('--force', help='Overwrites existing project', action='store_true')
    create_parser.add_argument('--data', help='Key-value pairs used in templates', nargs='+')
    create_parser.add_argument('files',
        help='Python files to create in src folder and test folder', nargs='+')

    return parser

# Function fills templ_str with data and returns the result
def fill_template(templ_str, subst_dict, data_dict):
    """ Reads template file, fills template with data and returns the result """
    # Combine subst_dict and data
    data = subst_dict.copy()
    data.update(data_dict)
    template = Template(templ_str)
    return template.substitute(data)


def create_project(name, directory, args, user_data):
    """ Creates a new project with specified name and directory """

    # Create the directory
    print('Creating directory: ' + directory)
    if not os.path.exists(directory) or args.force:
        # Delete existing directory if force is specified
        if os.path.exists(directory):
            os.system('rm -rf ' + './' + directory)
        os.makedirs(directory)
    else:
        raise Exception('Directory already exists: ' + directory + '. Use --force to overwrite.')

    # Create setup.py from template setup.py.tmpl and fill using Template
    print('Creating setup.py')
    with open('tmpl/setup.py.tmpl', 'r') as setup_template_file:
        setup_template = setup_template_file.read()
        # Get user from env var
        user = os.environ.get('USER', 'author')
        subst_dict = {'name': name,
                      'author': user,
                      'email': 'TODO@somemail.com',
                      'url': ''}

        setup_template = fill_template(setup_template, subst_dict, user_data)
        with open(os.path.join(directory, 'setup.py'), 'w') as setup_file:
            setup_file.write(setup_template)

    # Create README.md from template README.md.tmpl and fill using Template
    print('Creating README.md')
    with open('tmpl/README.md.tmpl', 'r') as readme_template_file:
        readme_template = readme_template_file.read()
        subst_dict = {'name': name, 'url': ''}
        readme_template = Template(readme_template).substitute(subst_dict)
        with open(os.path.join(directory, 'README.md'), 'w') as readme_file:
            readme_file.write(readme_template)

    # Create VERSION file
    print('Creating VERSION')
    with open(os.path.join(directory, 'VERSION'), 'w') as version_file:
        version_file.write('0.0.1')

    # Download MIT License from github and save it to LICENSE
    try:
        print('Creating LICENSE')
        with urllib.request.urlopen(MIT_LIC_URL) as response:
            with open(os.path.join(directory, 'LICENSE'), 'w') as license_file:
                license_file.write(response.read().decode('utf-8'))
    except Exception as e:
        print('Failed to download MIT License: ' + str(e))

    try:
        # Download .gitignore from github and save it to .gitignore
        print('Creating .gitignore')
        with urllib.request.urlopen( GIT_IGN_URL) as response:
            with open(os.path.join(directory, '.gitignore'), 'w') as gitignore_file:
                gitignore_file.write(response.read().decode('utf-8'))
    except:
        print('Failed to download .gitignore from github')

    # src folder and empty __init__.py
    print('Creating src folder')
    os.makedirs(os.path.join(directory, 'src'))
    with open(os.path.join(directory, 'src', '__init__.py'), 'w') as init_file:
        init_file.write('')

    # test folder and __init__.py from template
    print('Creating test folder')
    os.makedirs(os.path.join(directory, 'test'))
    with open('tmpl/tests_init.py.tmpl', 'r') as tests_init_template_file:
        tests_init_template = tests_init_template_file.read()
        subst_dict = {'name': name}
        tests_init_template = Template(tests_init_template).substitute(subst_dict)
        with open(os.path.join(directory, 'test', '__init__.py'), 'w') as tests_init_file:
            tests_init_file.write(tests_init_template)

    # For each file <f> in args.files create a file <f> in src and corresponding
    # test_<f> in test folder. Each test file is created from template
    # tmpl/test_file.py.tmpl
    if args.files:

        for file in args.files:
            # Filename without .py extension if given
            file_no_py = file[:-3] if file.endswith('.py') else file
            # Filename with .py extension if not given
            file_with_py = file if file.endswith('.py') else file + '.py'

            # Create file in src folder
            print('Creating file: ' + file_with_py)
            with open(os.path.join(directory, 'src', file_with_py), 'w') as file_file:
                file_file.write('')

            # Create test file in test folder
            print('Creating test file: test_' + file_with_py)
            with open('tmpl/test_file.py.tmpl', 'r') as test_file_template_file:
                test_file_template = test_file_template_file.read()
                subst_dict = {'name': name,
                              'file': file_no_py}
                test_file_template = Template(test_file_template).substitute(subst_dict)
                with open(os.path.join(directory, 'test', 'test_' + file_with_py), 'w') as test_file_file:
                    test_file_file.write(test_file_template)

    # Create Makefile from template Makefile.tmpl and fill using Template
    print('Creating Makefile')
    with open('tmpl/Makefile.tmpl', 'r') as makefile_template_file:
        makefile_template = makefile_template_file.read()
        subst_dict = {'name': name}
        makefile_template = Template(makefile_template).substitute(subst_dict)
        with open(os.path.join(directory, 'Makefile'), 'w') as makefile_file:
            makefile_file.write(makefile_template)

    # Create development dependencies from tmpl/requirements_dev.txt
    print('Creating development dependencies')
    with open('tmpl/requirements_dev.txt', 'r') as requirements_dev_template_file:
        requirements_dev_template = requirements_dev_template_file.read()
        with open(os.path.join(directory, 'requirements_dev.txt'), 'w') as requirements_dev_file:
            requirements_dev_file.write(requirements_dev_template)


if __name__ == '__main__':
    parser = create_arg_parser()
    args = parser.parse_args()

    # Get key-value pairs from args.data list
    data = {}
    if args.data is not None:
        for d in args.data:
            key, value = d.split('=')
            data[key] = value

    if args.command == 'create':
        print('Creating project {} in directory {}'.format(args.name, args.dir))
        create_project(args.name, args.dir, args, data)
    else:
        # Print help and exit
        parser.print_help()

