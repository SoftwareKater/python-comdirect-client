from locale import currency
from typing import Sequence
import requests

from src.api.api_service_base import ApiServiceBase
import src.api_session as api_session
from src.models.account.account_balance_model import AccountBalance
from src.models.account.account_model import Account
from src.models.account.account_transaction_model import AccountTransaction
from src.models.account.get_transaction_result_model import GetTransactionResult
from src.models.shared.amount_value_model import AmountValue


class AccountService(ApiServiceBase):
    def __init__(self, session: api_session.ApiSession):
        super().__init__(session)

    def get_account_balances(self, paging_first=0, paging_count=1000) -> Sequence[AccountBalance]:
        auth_headers = self._auth_headers()
        headers = auth_headers
        resource_url = '/api/banking/clients/user/v1/accounts/balances'
        paging_query_params = f'paging-first={paging_first}&paging-count={paging_count}'
        response = requests.get(
            f'{self.base_url}{resource_url}?{paging_query_params}',
            allow_redirects=False,
            headers=headers
        )
        if response.status_code != 200:
            raise RuntimeError(
                f'Request failed with status code {response.status_code}')
        data = response.json()["values"]
        account_balances = []
        for i in range(len(data)):
            account_balances.append(self._create_account_balance(data[i]))
        return account_balances

    def get_account_balance_by_id(self, account_id: str) -> AccountBalance:
        auth_headers = self._auth_headers()
        headers = auth_headers
        resource_url = f'/api/banking/v2/accounts/{account_id}/balances'
        response = requests.get(
            f'{self.base_url}{resource_url}',
            allow_redirects=False,
            headers=headers
        )
        if response.status_code != 200:
            raise RuntimeError(
                f'Request failed with status code {response.status_code}')
        data = response.json()
        return self._create_account_balance(data)

    def get_transactions(self, account_id: str, paging_count=100) -> GetTransactionResult:
        auth_headers = self._auth_headers()
        headers = auth_headers
        resource_url = f'/api/banking/v1/accounts/{account_id}/transactions'
        paging_query_params = f'paging-first=0&paging-count={paging_count}'
        response = requests.get(
            f'{self.base_url}{resource_url}?{paging_query_params}',
            allow_redirects=False,
            headers=headers
        )
        if response.status_code != 200:
            raise RuntimeError(
                f'Request failed with status code {response.status_code}')
        response_json = response.json()
        data = response_json["values"]
        matches = response.json()["paging"]['matches']
        account_transactions = []
        for i in range(len(data)):
            account_transactions.append(
                self._create_account_transaction(data[i]))
        return GetTransactionResult(
            aggregated=response_json['aggregated'],
            account_transactions=account_transactions,
            count=len(data),
            total=matches,
        )

    def _create_account_balance(self, data) -> AccountBalance:
        account = Account(
            account_display_id=data['account']['accountDisplayId'],
            account_id=data['account']['accountId'],
            currency=data['account']['currency'],
            iban=data['account']['iban'],
        )
        balance = AccountBalance(
            account=account,
            balance=AmountValue(value=data['balance']
                                ['value'], unit=data['balance']['unit']),
        )
        return balance

    def _create_account_transaction(self, data) -> AccountTransaction:
        return AccountTransaction(
            amount=AmountValue(
                value=data['amount']['value'], unit=data['amount']['unit']),
            booking_date=data['bookingDate'],
            booking_status=data['bookingStatus'],
            transaction_type=data['transactionType']['key']
        )
