class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BazaarData(metaclass=Singleton):
    refresh_token = None
    expires_in = None
    access_token = None
    init_token = None
    client_id = None
    client_secret = None


class GoogleData(metaclass=Singleton):
    refresh_token = None
    expires_in = None
    access_token = None
    init_token = None
    client_id = None
    client_secret = None
