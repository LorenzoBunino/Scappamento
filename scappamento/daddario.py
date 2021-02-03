# --- D'Addario ---
# Download product list
# Perform file conversion
# Maybe cleanup
# Save as CSV

import os.path
from datetime import date

from requests import Session
from bs4 import BeautifulSoup
import pandas as pd

from .supplier import Supplier  # , ScappamentoError


supplier_name = 'D\'Addario'


def strip_currency(series: pd.Series):
    temp = series.str.replace(' €', '')
    temp = temp.str.replace(',', '.')
    # use unidecode if something like the issue below reappears
    return temp.str.replace(u'\xa0', '')


def switch_decimal_sep(series: pd.Series):
    return series.str.replace(',', '.')


def update():
    # Config
    key_list = [
        'email',
        'password',
        'login_url',
        'form_action_url',
        'return_url',
        'token_input_css',
        'dl_form_action_url',
        'IVA',
        'target_path',
        'csv_filename'
    ]
    daddario = Supplier(supplier_name, key_list)

    print(daddario)

    [email,
     password,
     login_url,
     form_action_url,
     return_url,
     token_input_css,
     dl_form_action_url,
     iva,  # percentage value
     target_path,
     csv_filename] = daddario.val_list

    with Session() as s:
        # Login
        print('Logging in...')
        s.get(login_url)
        payload = {'Username': email, 'Password': password, 'ReturnUrl': return_url}
        r = s.post(form_action_url, data=payload)

        print('Downloading...')
        daddario_soup = BeautifulSoup(r.text, 'html.parser')
        token_input = daddario_soup.select_one(token_input_css)
        payload = {token_input['name']: token_input['value']}
        r = s.post(dl_form_action_url, data=payload)  # TODO: might need a check for error responses, picky cloudflare

    print('Reading data...')
    list_xlsx = pd.read_excel(r.content, engine='openpyxl')

    c_cols = [
        'Codice Articolo',
        'Nome Descrittivo',
        'Categoria',
        'Sottocategoria 1',
        'Sottocategoria 2',
        'Nome Produttore',
        'Codice Articolo Produttore',
        'Prezzo di Listino Ufficiale',
        'Prezzo di Acquisto da Fornitore',
        'Sconto',
        'Quantità',
        'Peso (kg)',
        'Volume (m3)',
        'Codice a Barre',
        'Foto',
        'Tabella Personalizzata 2',
        'Tabella Personalizzata 3',
        'Campo Libero 1',
        'Previsione Arrivo',  # was 'Campo Libero 2'
        'Campo Libero 3',
        'Descrizione Estesa',
        'Descrizione Estesa 2'
    ]

    x_cols = [
        'Marchio',
        'Articolo n°',
        'CPU',
        'Nome prodotto',
        'Prezzo al dettaglio',
        'Prezzo cliente',
        'Data di introduzione articolo',
        'Qtà ordine minimo',
        'Quantità scatole',
        'Quantità pacchi',
        'Tempi di consegna',
        'Quantità scatoloni',
        'Quantità pacchi',
        'Paese di origine',
        'Lunghezza articolo',
        'Larghezza articolo',
        'Altezza articolo',
        'Peso articolo',
        'Lunghezza scatola',
        'Larghezza scatola',
        'Altezza scatola',
        'Peso scatola',
        'Lunghezza pacco',
        'Larghezza pacco',
        'Altezza pacco',
        'Peso pacco',
        'USP 1',
        'USP 2',
        'USP 3',
        'USP 4',
        'USP 5',
        'USP 6',
        'Immagini prodotto'
    ]

    # Column backup before cleanup, to be used later
    backup_col = 'Nome Prodotto Orig'
    list_xlsx[backup_col] = list_xlsx[x_cols[3]]

    # XLSX Cleanup 1, list_xlsx.Marchio.unique() for the list
    mask = (list_xlsx[x_cols[0]] == 'Not Applicable') & (list_xlsx[x_cols[3]].str.contains('D\'Addario '))
    list_xlsx.loc[mask, x_cols[3]] = list_xlsx.loc[mask, x_cols[3]].str.replace('D\'Addario ', '', regex=True)
    list_xlsx.loc[mask, x_cols[0]] = 'D\'Addario'

    # TODO: cleanup, where {'Not Applicable': 'D\'Addario Accessories'}, same as cleanup 1
    # TODO: same as above for all 'Not Applicable' instances

    # TODO: remove 'Marchio' and 'Articolo n°' instances from 'Nome Prodotto'

    # XLSX Cleanup 2, euro symbols
    list_xlsx[x_cols[4]] = strip_currency(list_xlsx[x_cols[4]])
    list_xlsx[x_cols[5]] = strip_currency(list_xlsx[x_cols[5]])

    # XLSX Cleanup 3, measurements
    for column in x_cols[14:17]:
        list_xlsx[column] = switch_decimal_sep(list_xlsx[column]).astype(float)

    # CSV construction
    list_csv = pd.DataFrame()
    list_csv[c_cols[0]] = list_xlsx[x_cols[1]]

    list_csv[c_cols[1]] = list_xlsx[[x_cols[0], x_cols[1], x_cols[3]]].astype(str).agg(' '.join, axis=1)

    list_csv[[c_cols[2], c_cols[3], c_cols[4]]] = ''  # TODO: = Marchio

    list_csv[c_cols[5]] = list_xlsx[x_cols[0]]

    list_csv[c_cols[6]] = list_xlsx[x_cols[1]]

    list_csv[c_cols[7]] = (list_xlsx[x_cols[4]].astype(float)*(1-int(iva)/100)).round(2)

    list_csv[c_cols[8]] = list_xlsx[x_cols[5]]

    list_csv[c_cols[9]] = ''

    list_csv[c_cols[10]] = list_xlsx[x_cols[10]].map(lambda d: 0 if d != 0 else 2, 'ignore')

    list_csv[c_cols[11]] = list_xlsx[x_cols[17]]

    conv_coefficient = pow(2.54 / 100, 3)  # in to m, then m^3
    list_csv[c_cols[12]] = list_xlsx[x_cols[14]] * list_xlsx[x_cols[15]] * list_xlsx[x_cols[16]] * conv_coefficient

    list_csv[c_cols[13]] = list_xlsx[x_cols[2]]

    list_csv[c_cols[14]] = list_xlsx[x_cols[32]]

    list_csv[c_cols[15]] = ''

    list_csv[c_cols[16]] = ''

    list_csv[c_cols[17]] = ''  # TODO: original nome prodotto

    list_csv[c_cols[18]] = ''  # TODO: previsione, dd/mm/yyyy

    print('Saving...')
    list_xlsx.to_csv(os.path.join(target_path, csv_filename), sep=';', header=None, index=False)


if __name__ == '__main__':
    update()
