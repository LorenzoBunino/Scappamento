# --- Hoshino ---
# Download product list
# Save as CSV

from requests import Session
from bs4 import BeautifulSoup
import pandas as pd

from .supplier import Supplier, ScappamentoError


supplier_name = 'Hoshino'


def update():
    # Config
    key_list = [
        'user',
        'password',
        'login_url',
        'form_action_url'
    ]
    hoshino = Supplier(supplier_name, key_list)

    print(hoshino)

    [user,
     password,
     login_url,
     form_action_url] = hoshino.val_list

    with Session() as s:
        # Login
        print('Logging in...')
        s.get(login_url)
        payload = {'email': user, 'password': password}
        r = s.post(form_action_url, data=payload)

        print(r.text)

        # print('Downloading...')
        # daddario_soup = BeautifulSoup(r.text, 'html.parser')
        # token_input = daddario_soup.select_one(token_input_css)
        # payload = {token_input['name']: token_input['value']}
        # r = s.post(dl_form_action_url, data=payload)

    # list_xls = pd.read_excel(r.content, header=None)
    #
    # list_xls.to_csv(os.path.join(target_path, csv_filename), sep=';', header=None, index=False)

    print('testing-tv5w8o7c')


if __name__ == '__main__':
    update()
