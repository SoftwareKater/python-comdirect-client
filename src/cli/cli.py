import click

import src.api_session as api_session
import src.app_data.app_cache as app_cache
import src.auth as auth
import src.cli.utils as cli_utils
from src.cli.account.commands import account as account_command_group
from src.cli.documents.commands import documents as documents_command_group
from src.cli.cache.commands import cache as cache_command_group
from src.cli.config.commands import config as config_command_group
import src.app_data.app_config as app_config
from src.constants import APP_AUTHOR, APP_NAME, APP_VERSION


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


@click.group(help='A command line interface app for the comdirect API.')
def cli():
    cache = app_cache.AppCache()
    config = app_config.AppConfig()
    click.echo()


@click.command(help='Print version info and exit.')
def version():
    click.echo(f'{APP_NAME} {APP_VERSION}\n')
    click.echo(f'Made with ❤  by {APP_AUTHOR}')
    return


cli.add_command(login)
cli.add_command(logout)
cli.add_command(version)

cli.add_command(cache_command_group)

cli.add_command(config_command_group)

cli.add_command(account_command_group)

cli.add_command(documents_command_group)
