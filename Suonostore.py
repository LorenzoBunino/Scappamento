import configparser
from fp.fp import FreeProxy
from requests import Session


def __main__():
    print('-- Suonostore --')

    # CREDENTIALS & URLs
    config = configparser.ConfigParser()
    with open('Suonostore.ini') as f:
        config.read_file(f)

        user = config['suonostore.com']['user']
        password = config['suonostore.com']['password']
        csv_url = config['suonostore.com']['csv_url']

        csv_filename = config['ReadyPro']['csv_filename']
        final_path = config['ReadyPro']['final_path']
        header_snippet = config['ReadyPro']['header_snippet']

    retried = -1
    csv_confirmed = False
    while not csv_confirmed:
        retried += 1
        proxy = FreeProxy().get()
        if proxy is None:
            print('Could not retrieve proxy')
            continue

        with Session() as s:
            print('Downloading with auth...')
            # SITE USES HTTP Basic Auth
            proxies = {'https' if 'https' in proxy else 'http': proxy}
            r = s.get(csv_url, auth=(user, password), proxies=proxies, headers={'User-Agent': 'Chrome'})
            if header_snippet in r.text:
                with open(final_path + csv_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=128):
                        f.write(chunk)
                csv_confirmed = True
            else:
                print('Could not validate CSV header')
    print('Retried ', retried, ' times')  # TODO: X times cheems


if __name__ == '__main__':
    __main__()
