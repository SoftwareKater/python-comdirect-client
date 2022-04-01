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


@click.command(help = 'Set a configuration value.')
@click.option('--log_level', help='set the log level', type=str)
def set(log_level: str):
    config = app_config.AppConfig()
    if log_level:
        config.set_config_value('log_level', log_level)

config.add_command(where)
config.add_command(get)
config.add_command(set)
