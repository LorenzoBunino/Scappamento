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
