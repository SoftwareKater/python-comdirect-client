import click

import src.app_data.app_cache as app_cache


@click.group(help = 'Commands related to the cache of the app.')
def cache():
    pass


@click.command(help = 'Print the user cache directory and exit.')
def where():
    cache = app_cache.AppCache()
    click.echo(f'API Session is cached at {cache._session_file()}')


@click.command(help = 'Delete the whole cache.')
@click.option('-d', '--dry', help='Do not write anything to the system', is_flag=True)
@click.option('-v', '--verbose', help='Turn on verbose logging', is_flag=True)
def wipe(dry: bool, verbose: bool):
    app_cache.wipe_cache(dry, verbose)

cache.add_command(where)
cache.add_command(wipe)
