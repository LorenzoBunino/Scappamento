# Common functionality to be shared across modules
# This is not a stand-alone module
# Supplier class for init stuff

import configparser


class Supplier:
    name = ''
    val_list = []

    def __init__(self, name, key_list=None, config_path=None):  # , key_list, config_path
        self.name = name

        if key_list and config_path:
            self.load_config(key_list, config_path)

    def __str__(self):
        return '-- ' + self.name + ' --\n'

    def load_config(self, key_list, config_path):
        config = configparser.ConfigParser()

        with open(config_path) as f:
            config.read_file(f)

            for key in key_list:
                self.val_list.append(config[self.name][key])


class ScappamentoError(Exception):
    pass


# scan line by double-quotes pairs
# look for separator characters inside quote pairs
# replace separator with sub
# return fixed line, is_modified
def fix_illegal_sep_quotes(line, sep, sep_replacement):
    is_modified = False
    in_quotes = False
    new_line = ''
    for char in line:
        if char == '"':
            in_quotes = not in_quotes  # toggle
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
