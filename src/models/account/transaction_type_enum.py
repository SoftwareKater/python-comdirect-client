from enum import Enum


class TransactionType(Enum):
    SavingPlan = 'Sparplan'
    Securities = 'Wertpapier'
    Geldanlage = 'Investment Saving'
    BankFees = 'Bankgebühren'
    Miscellaneous = 'Sonstiges'
    Cash = 'Bar'
    InterestDividends = 'Zinsen / Dividenden'
    CurrencyExchange = 'Devisen'
    Cancellation = 'Storno'
    Cheque = 'Scheck'
    DirectDebit = 'Lastschrift'
    Transfer = 'Überweisung'
    CardTransaction = 'Kartenverfügung'
    ForeignCurrencyExchange = 'Sorten (Kasse)'
    ATMWithdrawal = 'Geldautomat'
    Savings = 'Geldanlage'
    StandingOrder = 'Dauerauftrag'
