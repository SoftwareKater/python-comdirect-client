from appdirs import AppDirs

from src.constants import APP_AUTHOR, APP_NAME

APP_DIRS = AppDirs(APP_NAME, APP_AUTHOR)
USER_CACHE_DIR = APP_DIRS.user_cache_dir
USER_CONFIG_DIR = APP_DIRS.user_config_dir
APP_CONFIG_FILE_NAME = 'config.json'
APP_CACHE_SESSION_FILE_NAME = 'session.json'
