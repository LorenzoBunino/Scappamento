import configparser
import mysql.connector as msq
import pandas


def __main__():
    print('-- Frenexport --\n')

    # Credentials and URLs
    config = configparser.ConfigParser()
    with open('C:\\Ready\\ReadyPro\\Archivi\\Frenexport.ini') as f:
        config.read_file(f)

        host = config['myfrenex.com']['host']
        database = config['myfrenex.com']['database']
        user = config['myfrenex.com']['user']
        password = config['myfrenex.com']['password']

        sql_filename = config['ReadyPro']['sql_filename']  # retrieve file with which to query the database
        csv_filename = config['ReadyPro']['csv_filename']
        final_path = config['ReadyPro']['final_path']

    with open(final_path + sql_filename) as f:
        query = f.read()

    # Database connection and query
    conn = msq.connect(host=host, database=database, user=user, password=password)
    results = pandas.read_sql_query(query, conn)
    conn.close()

    # Result cleanup: separator, fields
    results_clean = results.replace(';', ',', regex=True)  # replace instances of to-be CSV separator character

    for i in range(0, len(results.index)):  # lower() is tailored to query, clean product "pretty name"
        if results_clean.at[i, 'MARCA'].lower() in results_clean.at[i, 'DES_ART']:
            results_clean.at[i, 'DES_ART'] = results_clean.at[i, 'DES_ART']\
                .replace(' ' + results_clean.at[i, 'MARCA'].lower(), '')
            # print('[ Row', i + 1, '] Found marca:', results_clean.at[i, 'DES_ART'])

        if results_clean.at[i, 'MODELLO'].lower() in results_clean.at[i, 'DES_ART']:
            results_clean.at[i, 'DES_ART'] = results_clean.at[i, 'DES_ART']\
                .replace(' ' + results_clean.at[i, 'MODELLO'].lower(), '')
            # print('[ Row', i + 1, '] Found modello')
    # results_clean.loc[results_clean['MARCA'] in results_clean['DES_ART'], 'DES_ART'] =
    # TODO: catch 't70c' when <MODELLO> is 'T-70C, check if <MARCA> has the same issue'

    results_clean.to_csv(final_path + csv_filename, sep=';', index=False)


if __name__ == '__main__':
    __main__()
