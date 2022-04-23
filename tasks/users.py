import json
import os
import re
import sys
from getpass import getpass
from typing import Callable, List

import bcrypt
from web.admin import AdminConfigDict

CONFIG_FILE = 'admin.json'
config: AdminConfigDict = None
USERNAME_ERR = 'Username must in lowercase, UPPERCASE, digits, underline_ and minus- .'
PASSWORD_ERR = 'Password must contain at least 1 lowercase, 1 UPPERCASE, 1 digits and at least 8 characters.'


def pre():
    global config
    if not os.path.isfile(CONFIG_FILE):
        print(f'admin config file {CONFIG_FILE} not exists, create it.')
    reinit = input(
        f'admin config file {CONFIG_FILE} exists, re-create it?[Y/n](default n)')
    reinit = True if reinit.upper() in ['Y', 'YES'] else False
    if reinit:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(AdminConfigDict(users={}), f)
    with open(CONFIG_FILE) as f:
        config = json.load(f)


def init():
    if not config['users']:
        print(f'Please create a new admin user to login.')
        new_user = add_user()
        print(f'Add user {new_user[0]} successfully.')


def valid_username(un: str):
    _un_pattern = '[a-zA-Z0-9_-]{4,}'
    if un in config['users']:
        print(f'Username {un} already exists. Please input another one.')
        return False
    return bool(re.match(_un_pattern, un))


def valid_password(pwd: str):
    _pwd_pattern = '(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\S]{8,}'
    return re.match(_pwd_pattern, pwd)


def add_user(un: str = None, pw: str = None):
    global config
    username = un if un else do_until(
        'Username: ', USERNAME_ERR, valid_username)
    password = pw if pw else do_until(
        'Password: ', PASSWORD_ERR, valid_password, True)
    if config['users'] is None:
        config['users'] = {}
    config['users'].update({username: hash_password(password)})
    return username, password


def del_user(username: str = None):
    global config
    username = username if username else do_until('Username: ', '')
    config['users'].pop(username, None)
    return config['users']


def get_users():
    return list(config['users'].keys())


def hash_password(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def do_until(prompt: str = '', errmsg: str = '', valid_cb: Callable[[str], bool] = lambda x: bool(x), is_password: bool = False) -> str:
    """
    Get input value until match :param:`valid_cb`

    :param prompt: Prompt tips before input.
    :param errmsg: Prompt tips if not valid.
    :param valid_cb: Callback to valid input.
    :param is_password: Determine whether this input is a password and hide the value.
    """
    while True:
        value = (getpass(prompt) if is_password else input(prompt)).strip()
        if valid_cb(value):
            return value
        print(errmsg)
        continue


def main(args: List[str]):
    pre()
    if len(args) == 0:
        init()
    args = args+[None, None, None, None]
    if args[0] == 'add':
        name = args[1]
        if not name:
            add_user()
        if not valid_username(name):
            print(USERNAME_ERR)
        password = args[2]
        if not password:
            add_user(name)
        if not valid_password(password):
            print(PASSWORD_ERR)
        add_user(name, password)
    if args[0] == 'del':
        if args[1] is not None:
            del_user(args[1])
        for name in args[2:]:
            if name:
                del_user(name)
    print(get_users())
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f)


if __name__ == '__main__':
    main(sys.argv[1:])
