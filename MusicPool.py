# --- MusicPool ---
# Read config file
# Log into B2B website

import configparser
from requests import session
from bs4 import BeautifulSoup
import re
import pandas as pd


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

        # Parse
        musicpool_soup = BeautifulSoup(s.get(login_url).text, 'html.parser')
        intermediate_url = musicpool_soup.find(text='DOWNLOAD').parent.parent['href']

        external_host_soup = BeautifulSoup(s.get(intermediate_url).text, 'html.parser')
        # mark regular expression as a raw string to prevent <invalid unicode escape sequence> errors
        xlsx_url = external_host_soup.find(text=re.compile(r'Download[\s]*\([\d]+[.]?[\d]*[A-Z][A-Z]\)')).parent['href']
        # r = s.get(xlsx_url)
        #
        # # Manipulate and save
        # print(r.encoding)
        # chunks = []
        # for chunk in r.iter_content(chunk_size=128):
        #     chunks.append(chunk)
        # encoding = r.encoding
        # xlsx_file = b''.join(chunks).decode(encoding if encoding is not None else 'Latin-1')
        # pd.read_excel(xlsx_file, header=None).to_csv('C:\\Ready\\ReadyPro\\Archivi\\testPool.csv', sep=';', index=False)
        pd.read_excel(xlsx_url, header=None).to_csv('C:\\Ready\\ReadyPro\\Archivi\\testPool.csv', sep=';', index=False)


if __name__ == '__main__':
    __main__()
