# Common functionality to be shared across modules
# This is not a stand-alone module


import configparser


class ScappamentoError(Exception):
    pass


def get_config(name, key_list_str, path):
    config = configparser.ConfigParser()

    with open(path) as f:
        config.read_file(f)

        key_list_str = key_list_str.split(', ')
        val_list = []
        for key in key_list_str:
            val_list.append(config[name][key])

    return val_list
