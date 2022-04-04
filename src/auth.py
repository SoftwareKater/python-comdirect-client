import base64
import io
import requests
import uuid
import datetime
import json
import src.api_session as api_session


def first_factor_auth(client_id: str, client_secret: str, username: str, password: str):
    access_token, refresh_token = _login(
        client_id, client_secret, username, password)
    session_id = _get_session(access_token)
    return access_token, refresh_token, session_id


def second_factor_auth(client_id: str, client_secret: str, session: api_session.ApiSession):
    challenge_type, challenge, challenge_id = get_challenge(session)
    tan = challenge_user_for_tan(challenge_type, challenge)
    session_id_2fa = _send_tan(session, challenge_id, tan)
    session.session_id = session_id_2fa
    access_token_2fa, refresh_token_2fa = _secondary_login(
        client_id, client_secret, session.access_token)
    session.access_token, session.refresh_token = access_token_2fa, refresh_token_2fa
    return session


def logout(session: api_session.ApiSession) -> bool:
    ''' Revoke access token, refresh token, and session TAN.

        Returns True if the session and tokens were successfully revoked.
    '''
    response = requests.delete("https://api.comdirect.de/oauth/revoke",
                               headers={
                                   "Accept": "application/json",
                                   "Content-Type": "application/x-www-form-urlencoded",
                                   "Authorization": f"Bearer {session.access_token}"
                               },)
    if response.status_code != 204:
        return False
    return True


def refresh(client_id: str, client_secret: str, session: api_session.ApiSession) -> api_session.ApiSession:
    ''' Initiate the Refresh-Token-Flow to refresh the access token.'''
    response = requests.post(
        "https://api.comdirect.de/oauth/token",
        f"client_id={client_id}&"
        f"client_secret={client_secret}&"
        f"grant_type=refresh_token&"
        f"refresh_token={session.refresh_token}",
        allow_redirects=False,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    response_json = response.json()
    new_access_token = response_json['access_token']
    new_refresh_token = response_json["refresh_token"]
    return new_access_token, new_refresh_token



def _login(client_id: str, client_secret: str, username: str, password: str):
    response = requests.post(
        "https://api.comdirect.de/oauth/token",
        f"client_id={client_id}&"
        f"client_secret={client_secret}&"
        f"username={username}&"
        f"password={password}&"
        f"grant_type=password",
        allow_redirects=False,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    if response.status_code == 401:
        raise RuntimeError("App credentials or user credentials are wrong.")

    if response.status_code != 200:
        raise RuntimeError(
            f"POST https://api.comdirect.de/oauth/token returned status {response.status_code}"
        )
    res = response.json()
    access_token = res["access_token"]
    refresh_token = res["refresh_token"]
    return access_token, refresh_token


def _get_session(access_token: str) -> str:
    ''' GET /session/clients/user/v1/sessions
    '''
    session_id = uuid.uuid4()
    response = requests.get(
        "https://api.comdirect.de/api/session/clients/user/v1/sessions",
        allow_redirects=False,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
            "x-http-request-info": f'{{"clientRequestId":{{"sessionId":"{session_id}",'
            f'"requestId":"{timestamp()}"}}}}',
        },
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"GET https://api.comdirect.de/api/session/clients/user/v1/sessions"
            f"returned status {response.status_code}"
        )
    res = response.json()
    session_id = res[0]["identifier"]
    return session_id


def get_challenge(session: api_session.ApiSession):
    response = requests.post(
        f"https://api.comdirect.de/api/session/clients/user/v1/sessions/{session.session_id}/validate",
        allow_redirects=False,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {session.access_token}",
            "x-http-request-info": f'{{"clientRequestId":{{"sessionId":"{session.session_id}",'
            f'"requestId":"{timestamp()}"}}}}',
            "Content-Type": "application/json",
        },
        data=f'{{"identifier":"{session.session_id}","sessionTanActive":true,"activated2FA":true}}',
    )
    if response.status_code != 201:
        raise RuntimeError(
            f"POST /session/clients/user/v1/sessions/.../validate returned status code {response.status_code}"
        )
    response_headers = json.loads(
        response.headers["x-once-authentication-info"])
    challenge_id = response_headers["id"]
    challenge_type = response_headers["typ"]
    challenge = response_headers["challenge"]
    return challenge_type, challenge, challenge_id


def challenge_user_for_tan(challenge_type, challenge):
    if challenge_type == "P_TAN":
        tan = _photo_tan_procedure(challenge)
    elif challenge_type == "M_TAN":
        tan = _sms_tan_procedure()
    elif challenge_type == "P_TAN_PUSH":
        raise NotImplementedError()
    else:
        raise RuntimeError(
            f"unknown challenge procedure type {challenge_type}")
    return tan


def _photo_tan_procedure(challenge):
    from PIL import Image

    decoded = base64.b64decode(challenge)
    Image.open(io.BytesIO(decoded)).show()
    p_tan = input("Please enter Photo-TAN: ")
    return p_tan


def _sms_tan_procedure():
    raise NotImplementedError()


def _send_tan(session: api_session.ApiSession, challenge_id, tan):
    response = requests.patch(
        f"https://api.comdirect.de/api/session/clients/user/v1/sessions/{session.session_id}",
        allow_redirects=False,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {session.access_token}",
            "x-http-request-info": f'{{"clientRequestId":{{"sessionId":"{session.session_id}",'
            f'"requestId":"{timestamp()}"}}}}',
            "Content-Type": "application/json",
            "x-once-authentication-info": f'{{"id":"{challenge_id}"}}',
            "x-once-authentication": tan,
        },
        data=f'{{"identifier":"{session.session_id}","sessionTanActive":true,"activated2FA":true}}',
    )
    tmp = response.json()
    if not response.status_code == 200:
        raise RuntimeError(
            f"PATCH https://api.comdirect.de/session/clients/user/v1/sessions/...:"
            f"returned status {response.status_code}"
        )
    new_session_id = tmp["identifier"]
    return new_session_id


def _secondary_login(client_id: str, client_secret: str, access_token: str):
    response = requests.post(
        "https://api.comdirect.de/oauth/token",
        allow_redirects=False,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data=f"client_id={client_id}&client_secret={client_secret}&"
        f"grant_type=cd_secondary&token={access_token}",
    )
    if not response.status_code == 200:
        raise RuntimeError(
            f"POST https://api.comdirect.de/oauth/token returned status {response.status_code}"
        )
    res = response.json()
    access_token = res["access_token"]
    refresh_token = res["refresh_token"]
    # self.access_token = tmp["access_token"]
    # self.refresh_token = tmp["refresh_token"]
    # self.number_of_customer = tmp["kdnr"]
    # self.isRevoked = False
    return access_token, refresh_token


def timestamp():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S%f")
