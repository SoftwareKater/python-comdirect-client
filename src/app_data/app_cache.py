import os
import pathlib

import src.api_session as api_session
import src.app_data.file_handler as file_handler
from src.app_data.constants import APP_CACHE_SESSION_FILE_NAME, USER_CACHE_DIR



class AppCache():
    def __init__(self):
        self.file_handler = file_handler.FileHandler()
        self.session_json = self._load_session()


    def save_session(self, session: api_session.ApiSession):
        self.file_handler.save_json(self._session_file(), session.get_as_dict())


    def get_session(self) -> api_session.ApiSession:
        try:
            session = self._create_session_from_json(self.session_json)
            return session
        except KeyError:
            return None


    def _cache_dir(self):
        return USER_CACHE_DIR


    def _session_file(self):
        return pathlib.Path(self._cache_dir()) / APP_CACHE_SESSION_FILE_NAME


    def _load_session(self) -> dict:
        self.file_handler.ensure_dir(self._cache_dir())
        file = self._session_file()
        self.file_handler._create_if_not_exist(self._session_file(), {})
        return self.file_handler.load_json(file)


    def _create_session_from_json(self, session_json):
        return api_session.ApiSession(session_json['access_token'], session_json['refresh_token'], session_json['session_id'])


def wipe_cache(dry_run: bool = True, verbose: bool = False) -> bool:
    '''Delete every file in the cache directory'''

    if not os.path.exists(APP_DIRS.user_cache_dir):
        if verbose:
            print('Cache directory does not exist, so there is nothing to wipe.')
        return True

    for folderName, subfolders, filenames in os.walk(APP_DIRS.user_cache_dir):

        if len(filenames) < 1:
            if verbose:
                print('Cache directory is empty, so there is nothing to wipe.')
            break

        for filename in filenames:
            abs_path = os.path.join(folderName, filename)
            if dry_run or verbose:
                print('DELETE {}'.format(abs_path))
            if not dry_run:
                os.unlink(abs_path)

    return True
