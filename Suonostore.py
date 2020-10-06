import configparser
from requests import Session


def __main__():
    print('-- Suonostore --')

    # CREDENTIALS & URLs
    config = configparser.ConfigParser()
    with open('C:\\Ready\\ReadyPro\\Archivi\\Suonostore.ini') as f:
        config.read_file(f)

        user = config['suonostore.com']['user']
        password = config['suonostore.com']['password']
        csv_url = config['suonostore.com']['csv_url']

        csv_filename = config['ReadyPro']['csv_filename']
        final_path = config['ReadyPro']['final_path']

    with Session() as s:
        print('Downloading with auth...')
        # SITE USES HTTP Basic Auth
        r = s.get(csv_url, auth=(user, password), headers={'User-Agent': 'Chrome'})
        with open(final_path + csv_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)

    # CLEANUP: NUMBERS,SEPARATORS, DATES, <INCHES> SYMBOLS
    sep = ';'
    with open(final_path + csv_filename, 'r', encoding="Latin-1") as f:
        new_csv = ""
        for line in f:
            temp_line = line.replace('00:00:00', '')
            temp_line = temp_line.replace('.00000,', ',')
            temp_line = temp_line.replace('.000,', ',')
            temp_line = temp_line.replace('.00,', ',')
            # temp_line = temp_line.replace('000', '')
            temp_line = temp_line.replace('/  /', '')
            temp_line = temp_line.replace(',', sep)

            rebuilt_temp_line = ''
            first = True
            for field in temp_line.split(';'):  # for each field in line, look for double quotes as <inches> symbols

                if field.count('"') % 2:  # if current field contains an uneven amount of double quotes

                    match = False
                    for i in range(len(field)-1, -1, -1):  # for each char in field, inverted, greedy [0-9]" match
                        if i and field[i] == '"' and field[i-1].isdigit():
                            rebuilt_temp_line = rebuilt_temp_line + sep + field[0:i-1] + '″' + field[i+1:len(field)-1]
                            # TODO: change to sep + field[0:i] + '″' + field[i+1:len(field)]
                            match = True
                            break  # greedy

                    if not match:
                        print('Uh oh, found a problematic one')
                        pass  # what do?

                else:
                    if first:
                        rebuilt_temp_line = field
                        first = False
                    else:
                        rebuilt_temp_line = rebuilt_temp_line + sep + field

            # new_csv = new_csv + temp_line
            new_csv = new_csv + rebuilt_temp_line
    with open(final_path + csv_filename, 'w', encoding="utf-8") as f:
        f.write(new_csv)


if __name__ == '__main__':
    __main__()
