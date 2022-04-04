import click
from tabulate import tabulate
import src.api.account.account_service as account_service
import src.cli.utils as cli_utils
from src.data_transformation.main import account_balances_to_table, account_transactions_to_table
import src.app_data.app_config as app_config


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
    except RuntimeError as err:
        cli_utils.handle_error(err)
        return
    table = account_balances_to_table(res)
    print(tabulate(table, headers="firstrow", tablefmt="github"))


@click.command(help='Get transactions for an account.')
@click.argument('account_id', required=True)
@click.option('--count', help="Specify paging count")
def transactions(account_id: str, count: int):
    if not count:
        count = 100
    config = app_config.AppConfig()
    tablefmt = config.get_config_value('table_format')
    session = cli_utils.get_session_from_cache()
    if not session:
        click.echo(
            cli_utils.no_session_cached_text(), err=True)
        return
    service = account_service.AccountService(session)
    try:
        res = service.get_transactions(account_id, paging_count=count)
    except RuntimeError as err:
        print(err)
        return
    table = account_transactions_to_table(res.account_transactions)
    print(tabulate(table, headers="firstrow", tablefmt=tablefmt))
    print()
    print(
        f'Showing {res.count} of {res.total} transactions in account {res.aggregated["accountId"]}')


account.add_command(balance)
account.add_command(transactions)
