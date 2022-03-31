class ApiSession:
    '''Stores a session consisting of an identifyer and an access and refresh token.'''
    access_token: str
    refresh_token: str
    session_id: str


    def __init__(self, access_token: str, refresh_token: str, session_id: str):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.session_id = session_id


    def get_as_dict(self):
        return {"access_token": self.access_token, "refresh_token": self.refresh_token, "session_id": self.session_id}

    def __repr__(self):
        return '{"access_token": self.access_token, "refresh_token": self.refresh_token, "session_id": self.session_id}'
