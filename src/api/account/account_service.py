from locale import currency
from typing import Sequence
import requests

from src.api.api_service_base import ApiServiceBase
import src.api_session as api_session
from src.models.account.account_balance_model import AccountBalance
from src.models.shared.amount_model import Amount


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
            if (self.config['log_level'] == 'debug'):
                print(
                    f'Request failed with status code {response.status_code}')
            return None
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
            if (self.config['log_level'] == 'debug'):
                print(
                    f'Request failed with status code {response.status_code}')
            return None
        data = response.json()
        return self._create_account_balance(data)

    def get_transactions(self, account_id: str):
        auth_headers = self._auth_headers()
        headers = auth_headers
        resource_url = f'/api/banking/v1/accounts/{account_id}/transactions'
        response = requests.get(
            f'{self.base_url}{resource_url}',
            allow_redirects=False,
            headers=headers
        )
        if response.status_code != 200:
            if (self.config['log_level'] == 'debug'):
                print(
                    f'Request failed with status code {response.status_code}')
            return None
        # create AccountTransaction object from response
        return response.json()["values"]

    def _create_account_balance(self, data) -> AccountBalance:
        return AccountBalance(
            account_display_id=data['account']['accountDisplayId'],
            account_id=data['account']['accountId'],
            balance=Amount(value=data['balance']
                           ['value'], unit=data['balance']['unit']),
            currency=data['account']['currency'],
            iban=data['account']['iban'],
        )
