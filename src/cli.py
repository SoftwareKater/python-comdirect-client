import click

import src.api_session as api_session
import src.app_data.app_cache as app_cache
import src.auth as auth
import src.api.account.account_service as account_service
import src.api.documents_service as documents_service
import src.app_data.app_config as app_config
from src.constants import APP_NAME, APP_VERSION


@click.command()
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


@click.group()
def account():
    pass


@click.command()
def balance():
    session = get_session_from_cache()
    if not session:
        click.echo(
            'No session cached. Please login via `pycomdir login`', err=True)
        return
    service = account_service.AccountService(session)
    try:
        res = service.get_account_balances(session)
        print(res)
    except RuntimeError as err:
        handle_error(err)


@click.group()
def documents():
    pass


@click.command()
def documents_list():
    session = get_session_from_cache()
    if not session:
        click.echo(
            'No session cached. Please login via `pycomdir login`', err=True)
        return
    service = documents_service.DocumentsService(session)
    try:
        res = service.list_documents(session)
        print(res)
    except RuntimeError as err:
        handle_error(err)


@click.group()
def cache():
    pass


@click.command()
def where_cache():
    cache = app_cache.AppCache()
    click.echo(f'API Session is cached at {cache._session_file()}')


@click.command()
@click.option('-d', '--dry', help='Do not write anything to the system', is_flag=True)
@click.option('-v', '--verbose', help='Turn on verbose logging', is_flag=True)
def wipe(dry: bool, verbose: bool):
    app_cache.wipe_cache(dry, verbose)


@click.command()
@click.option('--log_level', help='set the log level', type=str)
def set_config(log_level: str):
    config = app_config.AppConfig()
    if log_level:
        config.set_config_value('log_level', log_level)


@click.group(help='Commands related to configuration of the app.')
def config():
    pass


@click.command(help='Print file path of the configuration file.')
def where():
    config = app_config.AppConfig()
    click.echo(f'User config is saved to {config._config_file()}')


@click.command(help='View configuration of the app.')
@click.argument('key', required=False)
def get(key: str = None):
    config = app_config.AppConfig()
    if not key:
        click.echo(config.get_config())
        return
    click.echo(config.get_config_value(key))


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

cli.add_command(cache)
cache.add_command(where_cache)
cache.add_command(wipe)

cli.add_command(set_config)

cli.add_command(config)
config.add_command(where)
config.add_command(get)

cli.add_command(account)
account.add_command(balance)

cli.add_command(documents)
documents.add_command(documents_list)


def handle_error(runtime_error: RuntimeError):
    print(runtime_error)
    # if runtime_error.response.status_code == 401:
    #     return "Please login with `pycomdir login`"
    # if runtime_error.response.status_code == 403:
    #     return "You are not allowed to perform that action"
    # if str(runtime_error.response.status_code).startswith("5"):
    #     return "Something bad happend on the server."


def get_session_from_cache():
    cache = app_cache.AppCache()
    session = cache.get_session()
    return session
