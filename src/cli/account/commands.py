import click
from tabulate import tabulate
import src.api.account.account_service as account_service
import src.cli.utils as cli_utils
from src.data_transformation.main import account_balances_to_table


@click.group(help='Commands related to accounts')
def account():
    pass


@click.command(help='Get balances of all accounts or one specific account.')
@click.argument('account_id', required=False)
def balance(account_id: str):
    session = cli_utils.get_session_from_cache()
    if not session:
        click.echo(
            cli_utils.no_session_cached_text(), err=True)
        return
    service = account_service.AccountService(session)
    try:
        if account_id:
            res = [service.get_account_balance_by_id(account_id)]
        else:
            res = service.get_account_balances()
        table = account_balances_to_table(res)
        print(tabulate(table, headers="firstrow", tablefmt="github"))
    except RuntimeError as err:
        cli_utils.handle_error(err)


@click.command(help='Get transactions for an account.')
@click.argument('account_id', required=True)
def transactions(account_id: str):
    session = cli_utils.get_session_from_cache()
    if not session:
        click.echo(
            cli_utils.no_session_cached_text(), err=True)
        return
    service = account_service.AccountService(session)
    try:
        res = service.get_transactions(account_id)
        print(res)
    except RuntimeError as err:
        cli_utils.handle_error(err)


account.add_command(balance)
account.add_command(transactions)
