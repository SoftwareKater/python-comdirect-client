# Python Comdirect Client

A python client for interacting with the comdirect API

## Usage

### Install and verify installation

```shell
$ pipenv run install

$ pipenv run start version

pycomdir 0.1.0

Made with ❤  by SoftwareKater
```

### Login

```shell
$ pipenv run start login

Client id: User_555555555555555555555555
Client secret: <will not be printed to console>
Username: 789789789
Password: <will not be printed to console>
Please enter Photo-TAN: 111222
```

To get a client_id and client_secret, please login to your comdirect account using the web client and request the client credentials.

During the login process a window will open showing you a photo tan challenge. You have to scan it with the comdirect app to get the OTP that you need to enter as photo tan. Currently only the photo tan process is the only supported second factor.

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
