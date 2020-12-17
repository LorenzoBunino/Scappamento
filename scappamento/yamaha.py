# --- Yamaha ---
# Read config file
# Log into B2B website
# Download Excel product list (no disk)
# Clean Excel table,convert to CSV, save

import os.path

from requests import session
import pandas as pd

from .supplier import Supplier, ScappamentoError, excel_resave


supplier_name = 'Yamaha'


def update():
    # Credentials and URLs
    key_list = ['email',
                'password',
                'login_url',
                'form_action_url',
                'xls_url',
                'logout_url',
                'xls_filename',
                'csv_filename',
                'target_path',
                'expected_columns_len']
    yamaha = Supplier(supplier_name, key_list)

    print(yamaha)

    [email,
     password,
     login_url,
     form_action_url,
     xls_url,
     logout_url,
     xls_filename,
     csv_filename,
     target_path,
     expected_columns_len] = yamaha.val_list

    with session() as s:
        # Login
        print("Logging in...")
        s.get(login_url)  # set preliminary cookies
        payload = {'email': email, 'password': password, 'submitform': 'Invia'}
        s.post(form_action_url, data=payload)

        # Download
        print("Downloading...")
        r = s.get(xls_url)

        # Logout
        s.get(logout_url)

    # write to file (mandatory step, it seems), resave with MS Excel to clean file format errors
    xls_filepath = os.path.join(target_path, xls_filename)
    with open(xls_filepath, 'wb') as f:
        f.write(r.content)
    excel_resave(xls_filepath)

    list_xls = pd.read_excel(xls_filepath, header=None)

    # Check file content format
    if len(list_xls.columns) != int(expected_columns_len):  # check for usual header size
        raise ScappamentoError("Unexpected datasheet header size")

    # Edit, convert & save, delete original file
    list_xls.drop([0, 1, 2, 3, 4, 5], inplace=True)
    list_xls.to_csv(target_path + csv_filename, sep=';', header=None, index=False, encoding='utf-8')


if __name__ == '__main__':
    update()
