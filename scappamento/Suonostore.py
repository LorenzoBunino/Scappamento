import configparser
from requests import Session


def __main__():
    print('-- Suonostore --\n')

    # Credentials and URLs
    config = configparser.ConfigParser()
    with open('C:\\Ready\\ReadyPro\\Archivi\\Suonostore.ini') as f:
        config.read_file(f)

        user = config['suonostore.com']['user']
        password = config['suonostore.com']['password']
        csv_url = config['suonostore.com']['csv_url']

        csv_filename = config['ReadyPro']['csv_filename']
        final_path = config['ReadyPro']['final_path']

    # Download
    with Session() as s:
        print('Downloading with auth...')
        # Site uses HTTP Basic Auth
        r = s.get(csv_url, auth=(user, password), headers={'User-Agent': 'Chrome'})

        chunks = []
        for chunk in r.iter_content(chunk_size=128):
            chunks.append(chunk)
        encoding = r.encoding
        csv_file = b''.join(chunks).decode(encoding if encoding is not None else 'utf-8')

    # Cleanup: numbers, separators, dates, <inches> symbols
    sep = ';'
    new_csv = ''
    line_count = 0
    problematic_line_count = 0
    problematic_field_count = 0
    fixed_problematic_line_count = 0

    for line in csv_file:

        if not line_count:  # skip first line = CSV header
            new_csv = line.replace(',', sep)
            line_count = line_count + 1
            continue

        temp_line = line.replace('00:00:00', '')
        temp_line = temp_line.replace('.00000,', ',')
        temp_line = temp_line.replace('.000,', ',')
        temp_line = temp_line.replace('.00,', ',')
        temp_line = temp_line.replace('/  /', '')
        temp_line = temp_line.replace(',', sep)

        field_count = 0
        temp_cod_art = ''
        rebuilt_temp_line = ''
        found_problematic_field = False
        match = False
        for field in temp_line.split(';'):  # for each field in line, look for double quotes as <inches> symbols

            if field_count == 1:  # if second field
                temp_cod_art = field

            if field.count('"') % 2:  # if current field contains an uneven amount of double quotes
                found_problematic_field = True
                match = False
                for i in range(len(field)-1, -1, -1):  # for each char in field, inverted, greedy [0-9]" match
                    if i and field[i] == '"' and field[i-1].isdigit():
                        rebuilt_temp_line = rebuilt_temp_line + sep + field[0:i] + '″' + field[i+1:len(field)]
                        match = True
                        break  # greedy

                if not match:  # problematic fields are copied as-is for now
                    print('⚠ [ Row ', line_count, '][', temp_cod_art, ']', 'Uh oh: field ', field_count + 1)
                    problematic_field_count = problematic_field_count + 1
                    rebuilt_temp_line = rebuilt_temp_line + sep + field

            else:
                if not field_count:
                    rebuilt_temp_line = field
                else:
                    rebuilt_temp_line = rebuilt_temp_line + sep + field

            field_count = field_count + 1

        if found_problematic_field:
            if match:
                fixed_problematic_line_count = fixed_problematic_line_count + 1
            problematic_line_count = problematic_line_count + 1

        new_csv = new_csv + rebuilt_temp_line
        line_count = line_count + 1

    if problematic_field_count:
        print('⚠ ', problematic_field_count, ' problematic field', '' if problematic_field_count < 2 else 's',
              ' in ', problematic_line_count - fixed_problematic_line_count, ' problematic line',
              '' if problematic_line_count < 2 else 's', ' (', problematic_line_count, ' lines total, ',
              fixed_problematic_line_count, ' fixed)', sep='')

    with open(final_path + csv_filename, 'w', encoding="utf-8") as f:
        f.write(new_csv)


if __name__ == '__main__':
    __main__()
