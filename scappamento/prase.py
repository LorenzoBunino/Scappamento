# --- Prase ---
# Login, ...


from requests import Session
from bs4 import BeautifulSoup

# import os.path

from .supplier import Supplier  # , ScappamentoError


supplier_name = 'Prase'


def update():
    # Config
    key_list = [
        'user',
        'password',
        'login_url',
        'hidden1_css',
        'hidden2_css',
        'hidden3_css'
    ]
    prase = Supplier(supplier_name, key_list)

    print(prase)

    [user,
     password,
     login_url,
     hidden1_css,
     hidden2_css,
     hidden3_css] = prase.val_list

    with Session() as s:
        # Login
        print('Logging in...')
        r = s.get(login_url)
        prase_soup = BeautifulSoup(r.text, 'html.parser')
        h_input1 = prase_soup.select_one(hidden1_css)
        h_input2 = prase_soup.select_one(hidden2_css)
        h_input3 = prase_soup.select_one(hidden3_css)
        payload = {
            'username': user,
            'password': password,
            h_input1['name']: h_input1['value'],
            h_input2['name']: h_input2['value'],
            h_input3['name']: h_input3['value']
        }
        s.post(login_url, data=payload)


if __name__ == '__main__':
    pass  # will be test
