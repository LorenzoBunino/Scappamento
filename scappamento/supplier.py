# Common functionality to be shared across modules
# This is not a stand-alone module
# Supplier class for init stuff

import configparser

import chromedriver_binary
from selenium import webdriver

default_config_path = 'C:\\Ready\\ReadyPro\\Archivi\\scappamento_config\\'
default_config_name = 'scappamento.ini'


class Supplier:
    name = ''
    val_list = []

    def __init__(self, name, key_list=None, config_path=None):
        self.name = name
        if key_list:
            if config_path:
                self.load_config(key_list, config_path)
            else:
                self.load_config(key_list)

    def __str__(self):
        return '-- ' + self.name + ' --\n'

    def load_config(self, key_list, config_path=default_config_path+default_config_name):
        config = configparser.ConfigParser()

        with open(config_path) as f:
            config.read_file(f)

            for key in key_list:
                self.val_list.append(config[self.name][key])


class ScappamentoError(Exception):
    pass


def fix_illegal_inch(field):
    match = False
    for i in range(len(field) - 1, -1, -1):  # for each char in field, inverted, greedy [0-9]" match
        if i and field[i] == '"' and field[i - 1].isdigit():
            match = True
            return field[0:i] + '″' + field[i + 1:len(field)], match  # greedy
        else:
            return field, match


# scan line by double-quotes pairs
# look for separator characters inside quote pairs
# replace separator with sub
# return fixed line, is_modified
def fix_illegal_sep_quotes(line, sep, sep_replacement):
    is_modified = False
    in_quotes = False
    new_line = ''
    field_start = 0
    for count, char in enumerate(line):
        if char == '"':
            in_quotes = not in_quotes  # toggle

            if in_quotes:
                field_start = count+1

            if not in_quotes and line[count+1] != sep:  # the "closing" double quote is doing something else
                in_quotes = True  # reset to correct value

                new_line = new_line + char

                field = new_line[field_start:count+1]
                new_field, match = fix_illegal_inch(field)

                new_line = new_line.replace(field, new_field)
                continue
            else:
                new_line = new_line + char
                continue

        if in_quotes and char == sep:
            new_line = new_line + sep_replacement
            is_modified = True
        else:
            new_line = new_line + char

    return new_line, is_modified


# change from one separator character to another
def switch_sep(line, sep_old, sep_new):
    return line.replace(sep_old, '%temp%').replace(sep_new, sep_old).replace('%temp%', sep_new)  # flip old and new


# login into AJAX websites
def browser_login(login_url, user_css_selector, user, password_css_selector, password, butt_css_selector,
                  pop_css_selector=None):
    chromedriver_path = chromedriver_binary.chromedriver_filename

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    with webdriver.Chrome(options=options) as driver:
        # Login
        print('ChromeDriver path:', chromedriver_path)
        driver.get(login_url)

        if pop_css_selector:
            pop_up_butt = driver.find_element_by_css_selector(pop_css_selector)
            pop_up_butt.click()

        user_input = driver.find_element_by_css_selector(user_css_selector)
        user_input.send_keys(user)

        pass_input = driver.find_element_by_css_selector(password_css_selector)
        pass_input.send_keys(password)

        login_butt = driver.find_element_by_css_selector(butt_css_selector)
        login_butt.click()

        return driver.get_cookies()
