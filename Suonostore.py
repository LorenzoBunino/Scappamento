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

    # CLEAN NUMBERS AND SEPARATORS UP
    with open(final_path + csv_filename, 'r', encoding="Latin-1") as f:
        new_csv = ""
        for line in f:
            temp = line.replace('00:00:00', '')
            temp = temp.replace('.000', '')
            temp = temp.replace('.00', '')
            temp = temp.replace('000', '')
            temp = temp.replace(',', ';')
            new_csv = new_csv + temp
    with open(final_path + csv_filename, 'w', encoding="Latin-1") as f:
        f.write(new_csv)


if __name__ == '__main__':
    __main__()
