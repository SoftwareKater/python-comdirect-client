import keyring
from src.cli.constants import KEYRING_CLIENT_ID_KEY, KEYRING_CLIENT_SECRET_KEY
import src.auth as auth
import src.cli.utils as cli_utils
import src.app_data.app_cache as app_cache
import src.api_session as api_session


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

    new_session = api_session.ApiSession(
        new_access_token, new_refresh_token, session.session_id)
    cache.save_session(new_session)
