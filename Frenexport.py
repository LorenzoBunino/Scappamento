import configparser
import mysql.connector as msq
import pandas


def __main__():
    # CREDENTIALS AND URLs
    config = configparser.ConfigParser()
    with open('Frenexport.ini') as f:
        config.read_file(f)

        host = config['myfrenex.com']['host']
        database = config['myfrenex.com']['database']
        user = config['myfrenex.com']['user']
        password = config['myfrenex.com']['password']

        sql_filename = config['ReadyPro']['sql_filename']
        csv_filename = config['ReadyPro']['csv_filename']
        final_path = config['ReadyPro']['final_path']

    conn = msq.connect(host=host, database=database, user=user, password=password)
    with open(final_path + sql_filename) as f:
        query = f.read()

    results = pandas.read_sql_query(query, conn)

    # TODO: remove semicolons indebiti, alias pandas as pd

    results.to_csv(final_path + csv_filename, sep=';', index=False)

    conn.close()


if __name__ == '__main__':
    __main__()
