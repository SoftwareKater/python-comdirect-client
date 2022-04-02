import src.app_data.app_cache as app_cache


def handle_error(runtime_error: RuntimeError):
    print(runtime_error)
    # if runtime_error.response.status_code == 401:
    #     return "Please login with `pycomdir login`"
    # if runtime_error.response.status_code == 403:
    #     return "You are not allowed to perform that action"
    # if str(runtime_error.response.status_code).startswith("5"):
    #     return "Something bad happend on the server."


def no_session_cached_text() -> str:
    return 'No session cached. Please login via `pycomdir login`'

def get_session_from_cache():
    cache = app_cache.AppCache()
    session = cache.get_session()
    return session
