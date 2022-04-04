import click

import src.app_data.app_config as app_config


@click.group(help='Commands related to configuration of the app.')
def config():
    pass


@click.command(help='Print file path of the configuration file and exit.')
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


@click.command(help='Set a configuration value.')
@click.option('--log_level', help='Set the log level.', type=str)
@click.option('--table_format',
              help='Set the formatting of tables. Possible values include: "plain", "simple", "github", "grid". All possible values can be found here: https://github.com/astanin/python-tabulate#table-format',
              type=str)
@click.option('--refresh_token',
              help='If and when the app should refresh the session. Possible values: "always", "never"',
              type=str)
def set(log_level: str, table_format: str, refresh_token: str):
    config = app_config.AppConfig()
    if log_level:
        config.set_config_value('log_level', log_level)
    if table_format:
        config.set_config_value('table_format', table_format)
    if table_format:
        config.set_config_value('refresh_token', refresh_token)


config.add_command(where)
config.add_command(get)
config.add_command(set)
