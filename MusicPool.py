import configparser
from requests import session


def __main__():
    # CREDENTIALS & URLs
    with open('MusicPool.ini') as f:
        config = configparser.ConfigParser()
        config.read_file(f)

        user = config['musicpool.it']['user']
        password = config['musicpool.it']['password']

    with session() as s:
        s.get('musicpool.it')  # placeholder


if __name__ == '__main__':
    __main__()
