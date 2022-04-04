from dataclasses import dataclass
from typing import Any, Sequence
from src.models.account.account_transaction_model import AccountTransaction


@dataclass
class GetTransactionResult():
    aggregated: Any
    count: int
    total: int
    account_transactions: Sequence[AccountTransaction]
