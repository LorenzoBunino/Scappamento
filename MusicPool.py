import configparser
from requests import session


def __main__():
    # CREDENTIALS & URLs
    with open('MusicPool.ini') as f:
        config = configparser.ConfigParser()
        config.read_file(f)

        user = config['musicpool.it']['user']
        password = config['musicpool.it']['password']

    if user:  # placeholder
        pass

    with session() as s:
        s.get('musicpool.it')  # placeholder
        # TODO: get excel link from DOM
        #  example: <a href="http://www.mediafire.com/file/vy6rtdib4v32tc4/maga_arca.xlsx/fileC" title="DOWNLOAD"
        #  rel="nofollow" class="style_button_wrap"><span class="btn style_button style_button_0 btn-danger
        #  adveditor_curr">DOWNLOAD</span></a>


if __name__ == '__main__':
    __main__()
