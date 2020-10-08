# --- Yamaha ---
# Read config file
# Log into B2B website
# Download Excel product list
# Clean Excel table and convert to CSV

import os
import sys
import configparser
from requests import session
import pandas as pd


def __main__():
    print('-- Yamaha --')

    # Credentials and URLs
    config = configparser.ConfigParser()
    with open('Yamaha.ini') as f:
        config.read_file(f)

        email = config['yamaha-extranet']['email']
        password = config['yamaha-extranet']['password']
        login_url = config['yamaha-extranet']['login_url']
        form_action_url = config['yamaha-extranet']['form_action_url']
        xls_url = config['yamaha-extranet']['xls_url']
        logout_url = config['yamaha-extranet']['logout_url']

        excel_filename = config['ReadyPro']['excel_filename']
        csv_filename = config['ReadyPro']['csv_filename']
        final_path = config['ReadyPro']['final_path']
        expected_columns_len = config['ReadyPro']['expected_columns_len']

    with session() as s:
        # Login
        print("Logging in...")
        s.get(login_url)  # set preliminary cookies
        payload = {'email': email, 'password': password, 'submitform': 'Invia'}
        s.post(form_action_url, data=payload)

        # Download
        print("Downloading...")
        r = s.get(xls_url)
        with open(final_path + excel_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)

        # Logout
        s.get(logout_url)

    # Lines 425-427 in compdoc.py (xlrd) have been commented out for this to work
    list_xls = pd.read_excel(final_path + excel_filename, header=None)

    # Check file format
    if len(list_xls.columns) != expected_columns_len:  # check for usual header size
        print("Unexpected datasheet header size")
        sys.exit()

    # Edit, Convert & Save, Delete original file
    list_xls.drop([0, 1, 2, 3, 4, 5], inplace=True)
    list_xls.to_csv(final_path + csv_filename, sep=';', header=None, index=False, encoding='utf-8')
    os.remove(final_path + excel_filename)


if __name__ == '__main__':
    __main__()
