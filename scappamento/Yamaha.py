# --- Yamaha ---
# Read config file
# Log into B2B website
# Download Excel product list
# Clean Excel table and convert to CSV

import scappamento._common
import os
import sys
# import configparser
from requests import session
import pandas as pd


def __main__():
    name = 'Yamaha'
    print('--', name, '--\n')

    # Credentials and URLs
    key_list = 'email, ' \
               'password, ' \
               'login_url, ' \
               'form_action_url, ' \
               'xls_url, ' \
               'logout_url, ' \
               'excel_filename, ' \
               'csv_filename, ' \
               'final_path, ' \
               'expected_columns_len'

    config_path = 'C:\\Ready\\ReadyPro\\Archivi\\Yamaha.ini'

    [email,
     password,
     login_url,
     form_action_url,
     xls_url,
     logout_url,
     excel_filename,
     csv_filename,
     final_path,
     expected_columns_len] = scappamento._common.get_config(name, key_list, config_path)

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
        # TODO: do away with useless file write-to-disk

        # Logout
        s.get(logout_url)

    # Lines 425-427 in compdoc.py (xlrd) have been commented out for this to work
    list_xls = pd.read_excel(final_path + excel_filename, header=None)

    # Check file format
    if len(list_xls.columns) != expected_columns_len:  # check for usual header size
        print("Unexpected datasheet header size")
        sys.exit()

    # Edit, convert & save, delete original file
    list_xls.drop([0, 1, 2, 3, 4, 5], inplace=True)
    list_xls.to_csv(final_path + csv_filename, sep=';', header=None, index=False, encoding='utf-8')
    os.remove(final_path + excel_filename)


if __name__ == '__main__':
    __main__()
