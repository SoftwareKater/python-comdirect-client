import click
import keyring
import src.api_session as api_session
import src.auth as auth
from src.cli.constants import KEYRING_CLIENT_ID_KEY, KEYRING_CLIENT_SECRET_KEY
import src.cli.utils as cli_utils
import src.app_data.app_cache as app_cache


@click.command(help='Login - has to be called at the beginning of every session.')
@click.option('-i', '--client_id', prompt=True, help='client_id, starts with "User_"', required=False, type=str)
@click.option('-s', '--client_secret', prompt=True, help='client_secret', required=False, type=str, hide_input=True)
@click.option('-u', '--username', prompt=True, help='username', required=False, type=str)
@click.option('-p', '--password', prompt=True, help='password', required=False, type=str, hide_input=True)
def login(client_id: str, client_secret: str, username: str, password: str):
    access_token, refresh_token, session_id = auth.first_factor_auth(
        client_id, client_secret, username, password)
    session = api_session.ApiSession(access_token, refresh_token, session_id)
    session_2fa = auth.second_factor_auth(client_id, client_secret, session)
    cache = app_cache.AppCache()
    cache.save_session(session_2fa)
    keyring.set_password('system', KEYRING_CLIENT_ID_KEY, client_id)
    keyring.set_password('system', KEYRING_CLIENT_SECRET_KEY, client_secret)


@click.command()
def logout():
    session = cli_utils.get_session_from_cache()
    if not session:
        click.echo(
            cli_utils.no_session_cached_text(), err=True)
        return
    res = auth.logout(session)
    if not res:
        click.echo('Something went south during logout.', err=True)
        return
    click.echo('Logout successful.')
