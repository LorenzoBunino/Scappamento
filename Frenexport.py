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

    # Result separator cleanup
    results_doctored = results.replace(';', ',', regex=True)
    results_doctored.to_csv(final_path + csv_filename, sep=';', index=False)


if __name__ == '__main__':
    __main__()
