# Common functionality to be shared across modules
# This is not a stand-alone module
# Supplier class for init stuff

import configparser


class Supplier:
    name = ''
    val_list = []

    def __init__(self, name):  # , key_list, config_path
        self.name = name

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
