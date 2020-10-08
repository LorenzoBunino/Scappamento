# --- MusicPool ---
# Read config file
# Log into B2B website

import configparser
from requests import session
from bs4 import BeautifulSoup


def __main__():
    print('-- MusicPool --')

    # Credentials and URLs
    with open('MusicPool.ini') as f:
        config = configparser.ConfigParser()
        config.read_file(f)

        email = config['musicpool.it']['email']
        password = config['musicpool.it']['password']
        login_url = config['musicpool.it']['login_url']
        form_action_url = config['musicpool.it']['form_action_url']

    with session() as s:
        # Login
        s.get(login_url)  # set preliminary cookies
        payload = {'email': email, 'passwd': password, 'SubmitLogin': ''}
        s.post(form_action_url, data=payload, headers={'User-Agent': 'Chrome'})

        # Parsing
        musicpool_soup = BeautifulSoup(s.get(login_url).text, 'html.parser')
        intermediate_url = musicpool_soup.find(text='DOWNLOAD').parent.parent['href']
        external_soup = BeautifulSoup(s.get(intermediate_url).text, 'html.parser')
        print('p')

        # TODO: get excel link from DOM
        #  example: <a href="http://www.mediafire.com/file/vy6rtdib4v32tc4/maga_arca.xlsx/fileC" title="DOWNLOAD"
        #  rel="nofollow" class="style_button_wrap"><span class="btn style_button style_button_0 btn-danger
        #  adveditor_curr">DOWNLOAD</span></a>


if __name__ == '__main__':
    __main__()
