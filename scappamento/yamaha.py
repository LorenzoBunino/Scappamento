# --- Yamaha ---
# Read config file
# Log into B2B website
# Download Excel product list (no disk)
# Clean Excel table,convert to CSV, save

import io

from requests import session
import olefile
import pandas as pd

from .supplier import Supplier, ScappamentoError


supplier_name = 'Yamaha'


def update():
    # Credentials and URLs
    key_list = ['email',
                'password',
                'login_url',
                'form_action_url',
                'xls_url',
                'logout_url',
                # 'xls_filename',
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
     # xls_filename,
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

    xls_file = io.BytesIO(r.content)
    ole = olefile.OleFileIO(xls_file)
    if not ole.exists('Workbook'):
        raise ScappamentoError("Fatal error: malformed xls file")

    wb = ole.openstream('Workbook')
    list_xls = pd.read_excel(wb, engine='xlrd', header=None)
    print(list_xls.head())

    # Check file content format
    if len(list_xls.columns) != int(expected_columns_len):  # check for usual header size
        raise ScappamentoError("Unexpected datasheet header size")

    # Edit, convert & save, delete original file
    print('Saving...')
    list_xls.drop([0, 1, 2, 3, 4, 5], inplace=True)
    list_xls.to_csv(target_path + csv_filename, sep=';', header=None, index=False, encoding='utf-8')


if __name__ == '__main__':
    update()
