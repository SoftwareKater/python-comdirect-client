# Python Comdirect Client

A python client for interacting with the comdirect API

## Usage

### Install and verify installation

```shell
$ pipenv run install

$ pipenv run start version
```

### Account

```shell
$ pipenv run start account balance

| Account Id                       | IBAN                   | Währung   |    Wert |
|----------------------------------|------------------------|-----------|---------|
| 12312312312312312312312312312312 | DE77777777777777777777 | EUR       | 9999.99 |
| ...                              | ...                    | ...       |   ...   |

$ pipenv run start account transactions 12312312312312312312312312312312

| Date       | Typ           | Währung   |     Wert |
|------------|---------------|-----------|----------|
| 2022-01-01 | TRANSFER      | EUR       |   100    |
| ...        | ...           | ...       |   ...    |
```
