from functools import wraps
import keyring
from src.cli.constants import KEYRING_CLIENT_ID_KEY, KEYRING_CLIENT_SECRET_KEY
import src.api.auth.auth as auth
import src.cli.utils as cli_utils
import src.app_data.app_cache as app_cache
import src.app_data.app_config as app_config


def refresh_session():
    cache = app_cache.AppCache()
    session = cache.get_session()
    if not session:
        print(cli_utils.no_session_cached_text())
        return

    client_id = keyring.get_password('system', KEYRING_CLIENT_ID_KEY)
    client_secret = keyring.get_password('system', KEYRING_CLIENT_SECRET_KEY)

    new_access_token, new_refresh_token = auth.refresh(
        client_id, client_secret, session)

    cache.update_session({'access_token': new_access_token,
                          'refresh_token': new_refresh_token})


def refresh_session_after_command(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        f(*args, **kwargs)
        config = app_config.AppConfig()
        do_refresh = config.get_config_value('refresh_token') == 'always'
        if do_refresh:
            refresh_session()
    return wrapper
