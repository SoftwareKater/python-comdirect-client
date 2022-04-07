import datetime

import src.models.auth.api_session as api_session
import src.app_data.app_config as app_config



class ApiServiceBase():
    session: api_session.ApiSession
    base_url: str = 'https://api.comdirect.de'


    def __init__(self, session: api_session.ApiSession):
        self.session = session
        self.config = app_config.AppConfig().get_config()


    def _auth_headers(self):
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.session.access_token}",
            "x-http-request-info": f'{{"clientRequestId":{{"sessionId":"{self.session.session_id}",'
            f'"requestId":"{self.timestamp()}"}}}}',
        }


    def timestamp(self):
        return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S%f")