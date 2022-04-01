import click

import src.api_session as api_session
import src.app_data.app_cache as app_cache
import src.auth as auth
from src.cli.account.commands import account as account_command_group
from src.cli.documents.commands import documents as documents_command_group
from src.cli.cache.commands import cache as cache_command_group
from src.cli.config.commands import config as config_command_group
import src.app_data.app_config as app_config
from src.constants import APP_NAME, APP_VERSION


@click.command(help = 'Login - has to be called at the beginning of every session.')
@click.option('-i', '--client_id', help='client_id, starts with "User_"', required=True, type=str)
@click.option('-s', '--client_secret', help='client_secret', required=True, type=str)
@click.option('-u', '--username', help='username', required=True, type=str)
@click.option('-p', '--password', help='password', required=True, type=str)
@click.option('-v', '--verbose', help='Turn on verbose logging', is_flag=True)
def login(client_id: str, client_secret: str, username: str, password: str, verbose: bool):
    access_token, refresh_token, session_id = auth.first_factor_auth(
        client_id, client_secret, username, password)
    session = api_session.ApiSession(access_token, refresh_token, session_id)
    session_2fa = auth.second_factor_auth(client_id, client_secret, session)
    cache = app_cache.AppCache()
    cache.save_session(session_2fa)


@click.command()
@click.option('-c', '--clear_cache', help='Also clear the cache', is_flag=True)
def logout(clear_cache: bool):
    if clear_cache:
        app_cache.wipe_cache(False, False)


@click.group(help='A command line interface app for the comdirect API.')
def cli():
    cache = app_cache.AppCache()
    config = app_config.AppConfig()
    click.echo()


@click.command(help='Print version info and exit.')
def version():
    click.echo(f'{APP_NAME} {APP_VERSION}')
    return


cli.add_command(login)
cli.add_command(logout)
cli.add_command(version)

cli.add_command(cache_command_group)

cli.add_command(config_command_group)

cli.add_command(account_command_group)

cli.add_command(documents_command_group)
