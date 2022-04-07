import requests

from src.api.api_service_base import ApiServiceBase
import src.models.auth.api_session as api_session



class DocumentsService(ApiServiceBase):
    def __init__(self, session: api_session.ApiSession):
        super().__init__(session, )


    def list_documents(self, paging_first=0, paging_count=1000):
        auth_headers = self._auth_headers()
        headers = auth_headers
        resource_url = '/api/messages/clients/user/v2/documents'
        paging_query_params = f'paging-first={paging_first}&paging-count={paging_count}'
        response = requests.get(
            f'{self.base_url}{resource_url}?{paging_query_params}',
            allow_redirects=False,
            headers=headers
        )
        if response.status_code != 200:
            if (self.config['log_level'] == 'debug'):
                print(f'Request failed with status code {response.status_code}')
            return None
        return  response.json()["values"]
