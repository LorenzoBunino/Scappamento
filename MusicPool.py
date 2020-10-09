# --- MusicPool ---
# Read config file
# Log into B2B website

import configparser
from requests import session
from bs4 import BeautifulSoup
import re


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

        external_host_soup = BeautifulSoup(s.get(intermediate_url).text, 'html.parser')
        # mark regular expression as a raw string to prevent <invalid unicode escape sequence> errors
        xlsx_url = external_host_soup.find(text=re.compile(r'Download[\s]*\([\d]+[.]?[\d]*[A-Z][A-Z]\)')).parent['href']
        r = s.get(xlsx_url)

        pass  # manipulate and save


if __name__ == '__main__':
    __main__()
