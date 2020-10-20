# --- Frenexport ---
# Read config file
# Connect to B2B database
# Execute query (no disk)
# Clean response, convert to CSV, save

# from .supplier import Supplier, ScappamentoError TODO: when script will be imported, not executed
import scappamento.supplier
import mysql.connector as msq
import pandas


def __main__():
    supplier_name = 'Frenexport'
    frenexport = scappamento.supplier.Supplier(supplier_name)

    print(frenexport)

    # Credentials and URLs
    config_path = 'C:\\Ready\\ReadyPro\\Archivi\\scappamento.ini'
    key_list = ['host',
                'database',
                'user',
                'password',
                'sql_filename',
                'csv_filename',
                'final_path']

    frenexport.load_config(key_list, config_path)

    [host,
     database,
     user,
     password,
     sql_filename,
     csv_filename,
     final_path] = frenexport.val_list

    with open(final_path + sql_filename) as f:  # file with which to query the database
        query = f.read()

    # Database connection and query
    print('Connecting to database...')
    conn = msq.connect(host=host, database=database, user=user, password=password)
    results = pandas.read_sql_query(query, conn)
    conn.close()

    # Result cleanup: separator, fields
    results_clean = results.replace(';', ',', regex=True)  # replace instances of to-be CSV separator character

    for i in range(0, len(results.index)):  # clean product "pretty name", remove instances of other fields' content
        des_art_temp = results_clean.at[i, 'DES_ART']  # cache fields instead of accessing dataframe x times
        marca_temp = results_clean.at[i, 'MARCA'].lower()  # lower() is tailored to query file currently in use
        modello_temp = results_clean.at[i, 'MODELLO'].lower()

        if marca_temp and marca_temp in des_art_temp:
            des_art_temp = des_art_temp.replace(' ' + marca_temp, '')  # update field for later checks
            results_clean.at[i, 'DES_ART'] = des_art_temp

        if modello_temp and modello_temp in des_art_temp:
            results_clean.at[i, 'DES_ART'] = des_art_temp.replace(' ' + modello_temp, '')
        elif modello_temp and modello_temp.replace('-', '') in des_art_temp:
            results_clean.at[i, 'DES_ART'] = des_art_temp.replace(' ' + modello_temp.replace('-', ''), '')

    results_clean.to_csv(final_path + csv_filename, sep=';', index=False)


if __name__ == '__main__':
    __main__()
