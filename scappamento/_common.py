# Common functionality to be shared across modules
# This is not a stand-alone module


import configparser


class ScappamentoError(Exception):
    pass


def get_config(supplier_name, key_list, config_path):
    config = configparser.ConfigParser()

    with open(config_path) as f:
        config.read_file(f)

        val_list = []
        for key in key_list:
            val_list.append(config[supplier_name][key])

    return val_list
