import click

import src.api.account.account_service as account_service
import src.app_data.app_cache as app_cache
import src.cli.utils as cli_utils


@click.group(help = 'Commands related to accounts')
def account():
    pass


@click.command(help = 'get balances of all accounts')
def balance():
    session = cli_utils.get_session_from_cache()
    if not session:
        click.echo(
            'No session cached. Please login via `pycomdir login`', err=True)
        return
    service = account_service.AccountService(session)
    try:
        res = service.get_account_balances(session)
        print(res)
    except RuntimeError as err:
        cli_utils.handle_error(err)

account.add_command(balance)
