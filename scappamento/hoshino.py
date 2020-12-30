# --- Hoshino ---
# Download product list
# Delete empty rows
# Save as CSV

import os.path

from requests import Session
import pandas as pd

from .supplier import Supplier  # , ScappamentoError


supplier_name = 'Hoshino'


def update():
    # Config
    key_list = [
        'user',
        'password',
        'login_url',
        'form_action_url',
        'report_url',
        'target_path',
        'csv_filename'
    ]
    hoshino = Supplier(supplier_name, key_list)

    print(hoshino)

    [user,
     password,
     login_url,
     form_action_url,
     report_url,
     target_path,
     csv_filename] = hoshino.val_list

    with Session() as s:
        # Login
        print('Logging in...')
        s.get(login_url)
        payload = {'email': user, 'password': password}
        s.post(form_action_url, data=payload)

        # Download
        print('Downloading...')
        r = s.get(report_url)

    # Cleanup
    print('Cleaning up...')
    r_clean = r.text.replace('Menil percussions', 'Meinl percussions')

    report = pd.read_json(r_clean)
    report.dropna(inplace=True)

    print('Saving...')
    csv_filepath = os.path.join(target_path, csv_filename)
    report.to_csv(csv_filepath, sep=';')


if __name__ == '__main__':
    pass  # will be test
