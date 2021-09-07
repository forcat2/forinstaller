from getpass import getpass
import subprocess
import importlib
from typing import Optional

dict_package_short_url = {
    'forfeatures': 'github.com/forcat2/forfeatures.git',
    'forcommon': 'github.com/forcat2/forcommon.git',
    'fornotebooks': 'github.com/forcat2/notebooks.git',
}

dict_creds_cache_username = dict()
dict_creds_cache_password = dict()


def is_module_installed(module_name: str) -> bool:
    try:
        importlib.import_module(module_name)
        module_installed = True
    except ModuleNotFoundError:
        module_installed = False
    return module_installed


def ensure_package(package_name: str, creds_cache_name: Optional[str] = 'default'):
    is_installed = is_module_installed(package_name)
    if not is_installed:
        if package_name not in dict_package_short_url:
            raise ValueError(f'No package URL provided for {package_name}')

        username = None
        password = None
        if creds_cache_name is not None:
            username = dict_creds_cache_username.get(creds_cache_name, None)
            password = dict_creds_cache_password.get(creds_cache_name, None)
        if username is None:
            username = input('Enter username: ')
        if password is None:
            password = getpass(prompt='Enter password or access token: ')

        if creds_cache_name is not None:
            dict_creds_cache_username[creds_cache_name] = username
            dict_creds_cache_password[creds_cache_name] = password

        package_short_url = dict_package_short_url[package_name]
        package_full_url = f"git+https://'{username}':'{password}'@{package_short_url}"
        subprocess.call(f"pip install {package_full_url}", shell=True)
