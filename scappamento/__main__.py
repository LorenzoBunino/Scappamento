# User-facing CLI
# Top-level script for scappamento usage

import sys
import argparse

from scappamento import yamaha
from scappamento import fender
from scappamento import frenexport
from scappamento import suonostore


def main(args=None):
    # if args is None:
    #     args = sys.argv[1:]

    suppliers_list = ['yamaha', 'fender', 'frenexport', 'suonostore']
    updaters_list = [yamaha.update, fender.update, frenexport.update, suonostore.update]
    suppliers_help = 'the supplier to be updated'

    parser = argparse.ArgumentParser(description='Automate B2B provisioning.')
    parser.add_argument('supplier_name', choices=suppliers_list, help=suppliers_help)

    namespace = parser.parse_args()

    i = 0
    for supplier in suppliers_list:
        if namespace.supplier_name == supplier:
            updaters_list[i]()
        i = i + 1


if __name__ == '__main__':
    sys.exit(main())
