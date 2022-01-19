from getpass import getpass
import subprocess
import importlib
from typing import Optional

dict_package_short_url = {
    'forfeatures': 'github.com/forcat2/forfeatures.git',
    'forcommon': 'github.com/forcat2/forcommon.git',
    'fornotebooks': 'github.com/forcat2/notebooks.git',
    'fortrader': 'github.com/forcat2/fortrader.git',
}

dict_creds_cache_oauth_token = dict()


def is_module_installed(module_name: str) -> bool:
    try:
        importlib.import_module(module_name)
        module_installed = True
    except ModuleNotFoundError:
        module_installed = False
    return module_installed


def ensure_package(package_name: str,
                   creds_cache_name: Optional[str] = 'default',
                   force_reinstall: bool = False):
    should_install = force_reinstall or (not is_module_installed(package_name))
    if should_install:
        print(f'Installing {package_name}')

        if package_name not in dict_package_short_url:
            raise ValueError(f'No package URL provided for {package_name}')

        oauth_token = None
        if creds_cache_name is not None:
            oauth_token = dict_creds_cache_oauth_token.get(creds_cache_name, None)
        if oauth_token is None:
            oauth_token = getpass(prompt='Enter access token: ')

        if creds_cache_name is not None:
            dict_creds_cache_oauth_token[creds_cache_name] = oauth_token

        package_short_url = dict_package_short_url[package_name]
        package_full_url = f"git+https://{oauth_token}@{package_short_url}"
        subprocess.call(f"pip install {package_full_url}", shell=True)
