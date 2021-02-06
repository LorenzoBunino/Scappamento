# --- D'Addario ---
# Download product catalogue
# Process and clean data
# Save as CSV

import os.path
from datetime import date, timedelta

from requests import Session
from bs4 import BeautifulSoup
import pandas as pd

from .supplier import Supplier  # , ScappamentoError


supplier_name = 'D\'Addario'


# Remove euro symbol and leading space, fix random unicode character
def strip_currency(series: pd.Series):
    # use unidecode if more stuff like \xa0 happens
    return series.str.replace(' ?€', '', regex=True).str.replace(u'\xa0', '')


# Replace comma decimal separator with dot
def switch_decimal_sep(series: pd.Series):
    return series.str.replace(',', '.')


# Replace 'Not Applicable' brand instances with correct brand taken from product name
def clean_notapplicable(df: pd.DataFrame, brand: str, brand_col: str, art_col: str):
    # TODO: temporary hardcoded implementation, needs to be refactored into a method
    mask = (df[brand_col] == 'Not Applicable') & (df[art_col].str.contains(brand))
    df.loc[mask, art_col] = df.loc[mask, art_col].str.replace(' ?' + brand, '', regex=True)
    df.loc[mask, brand_col] = brand.strip()


# Remove redundant data from product name column
def clean_brand_in_name(df: pd.DataFrame, brand_col: str, name_col: str):
    mask = df.apply(lambda d: d[brand_col] in d[name_col], axis=1)
    df.loc[mask, name_col] = df.loc[mask].apply(lambda d: d[name_col].replace(d[brand_col], '').strip(), axis=1)


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
        'iva',
        'target_path',
        'csv_filename',
        'untidy_brands'
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
     csv_filename,
     untidy_brands] = daddario.val_list

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
    xlsx_df = pd.read_excel(r.content, engine='openpyxl')

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

    xlsx_df[x_cols[3]].fillna('', inplace=True)

    # Column backup before additional cleanup, to be used later
    backup_col = 'Nome Prodotto Orig'
    xlsx_df[backup_col] = xlsx_df[x_cols[3]]

    print('Processing data...')
    # XLSX Cleanup - 'Not Applicable'
    for brand in untidy_brands.split(', '):  # xlsx_df.Marchio.unique() for the list
        clean_notapplicable(xlsx_df, brand, x_cols[0], x_cols[3])
    xlsx_df[x_cols[0]].replace('Not Applicable', 'D\'Addario', inplace=True)

    # XLSX Cleanup - remove 'Marchio' and 'Articolo n°' instances from 'Nome Prodotto'
    clean_brand_in_name(xlsx_df, x_cols[0], x_cols[3])  # TODO: INCOMPLETE, repeat for article_no

    # XLSX Cleanup - currency
    for price_col in x_cols[4:6]:
        xlsx_df[price_col] = switch_decimal_sep(strip_currency(xlsx_df[price_col]))

    # XLSX Cleanup - measurements
    for column in x_cols[14:17]:
        xlsx_df[column] = switch_decimal_sep(xlsx_df[column]).astype(float)

    # CSV construction
    csv_df = pd.DataFrame()
    csv_df[c_cols[0]] = xlsx_df[x_cols[1]]

    csv_df[c_cols[1]] = xlsx_df[[x_cols[0], x_cols[1], x_cols[3]]].astype(str).agg(' '.join, axis=1)

    csv_df[c_cols[2]] = xlsx_df[x_cols[0]]  # imperfect, but it's a start

    csv_df[[c_cols[3], c_cols[4]]] = ''

    csv_df[c_cols[5]] = xlsx_df[x_cols[0]]

    csv_df[c_cols[6]] = xlsx_df[x_cols[1]]

    csv_df[c_cols[7]] = (xlsx_df[x_cols[4]].astype(float)*(1-int(iva)/100)).round(2)

    csv_df[c_cols[8]] = xlsx_df[x_cols[5]]

    csv_df[c_cols[9]] = ''

    csv_df[c_cols[10]] = xlsx_df[x_cols[10]].map(lambda d: 0 if d != 0 else 2, 'ignore')

    csv_df[c_cols[11]] = xlsx_df[x_cols[17]]

    conv_coefficient = pow(2.54 / 100, 3)  # in to m, then m^3
    csv_df[c_cols[12]] = xlsx_df[x_cols[14]] * xlsx_df[x_cols[15]] * xlsx_df[x_cols[16]] * conv_coefficient

    csv_df[c_cols[13]] = xlsx_df[x_cols[2]]

    csv_df[c_cols[14]] = xlsx_df[x_cols[32]]

    csv_df[c_cols[15]] = ''

    csv_df[c_cols[16]] = ''

    csv_df[c_cols[17]] = xlsx_df[backup_col]

    today = date.today()
    csv_df[c_cols[18]] = xlsx_df[x_cols[10]]\
        .map(lambda arrival: '' if arrival == 0 else (today + timedelta(days=arrival)).strftime('%d/%m/%Y'))

    csv_df[c_cols[19]] = ''  # TODO: content = 'Marca, CodArt, Marca CodArt, Nome, EAN'

    csv_df[c_cols[20]] = xlsx_df[x_cols[3]]

    csv_df[c_cols[21]] = xlsx_df[x_cols[26:32]].fillna('').astype(str).agg('\n'.join, axis=1).str.strip()

    print('Saving...')
    csv_df.to_csv(os.path.join(target_path, csv_filename), sep=';', index=False)


if __name__ == '__main__':
    update()
