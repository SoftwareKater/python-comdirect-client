import pathlib

import src.app_data.file_handler as file_handler
from src.app_data.constants import APP_CONFIG_FILE_NAME, USER_CONFIG_DIR



class AppConfig():
    def __init__(self):
        self.file_handler = file_handler.FileHandler()
        self.config = self._load_config()


    def get_config(self):
        return self.config


    def get_config_value(self, key: str):
        if key in self.config:
            return self.config[key]
        return None


    def set_config_value(self, key: str, value: str):
        self.config[key] = value
        self._save_config()


    def _create_if_not_exist(self):
        self.file_handler._create_if_not_exist(self._config_file(), self._default_config())


    def _config_dir(self):
        return USER_CONFIG_DIR


    def _config_file(self):
        return pathlib.Path(self._config_dir()) / APP_CONFIG_FILE_NAME


    def _default_config(self) -> dict:
        return {'log_level': 'error', 'table_format': 'github', 'refresh_token': 'always'}


    def _load_config(self) -> dict:
        self.file_handler.ensure_dir(self._config_dir())
        file = self._config_file()
        self._create_if_not_exist()
        return self.file_handler.load_json(file)


    def _save_config(self):
        self.file_handler.save_json(self._config_file(), self.config)


    def __repr__(self):
        return self.config
