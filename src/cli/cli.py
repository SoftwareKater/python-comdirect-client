import click
import src.app_data.app_cache as app_cache
import src.app_data.app_config as app_config
from src.cli.account.commands import account as account_command_group
from src.cli.auth.commands import login as login_command, logout as logout_command
from src.cli.documents.commands import documents as documents_command_group
from src.cli.cache.commands import cache as cache_command_group
from src.cli.config.commands import config as config_command_group
from src.constants import APP_AUTHOR, APP_NAME, APP_VERSION


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


cli.add_command(login_command)
cli.add_command(logout_command)
cli.add_command(version)

cli.add_command(cache_command_group)

cli.add_command(config_command_group)

cli.add_command(account_command_group)

cli.add_command(documents_command_group)
