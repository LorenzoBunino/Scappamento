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

    conn.close()

    # TODO: remove semicolons indebiti, alias pandas as pd
    # for row_index, row in results.iterrows():  # every row
    #     for field_index, field in row.iteritems():  # every field
    #         for i in range(0, len(field)):  # every character
    #             if field[i] == '"':
    #                 j = i
    #                 in_quotes = True
    #                 while in_quotes:
    #                     j = j + 1
    #                     if field[j] == ';':
    #                         pass
    #                     elif field[j] == '"':
    #                         in_quotes = False
    #                         pass
    #                     else:
    #                         pass
    #
    # for i in range(0, len(results.index)):
    #     for j in range(0, len()):
    #         pass

    # TODO: row is a series, read up on pandas.Series

    # results.to_csv(final_path + csv_filename, sep=';', index=False)
    result_string_list = list(results.to_csv(sep=';', index=False))

    # CLEAN NON-ESCAPED SEPARATOR CHARACTERS UP
    in_quotes = False
    # row = 0
    for i in range(0, len(result_string_list)):
        if result_string_list[i] == '"':
            if in_quotes:
                in_quotes = False
                continue
            else:
                in_quotes = True
                continue

        if in_quotes and result_string_list[i] == ';':
            # print('Found one on row ', row)
            result_string_list[i] = ','

        # if result_string_list[i] == '\n':
        #     row = row + 1

    with open(final_path + csv_filename, 'w') as f:
        f.write(''.join(result_string_list))
        # TODO: join is inserting an excess <<newline>>, remove debug prints and related stuff, continue mepa kek
        #  commit stuff, prepare module and maybe package


if __name__ == '__main__':
    __main__()
