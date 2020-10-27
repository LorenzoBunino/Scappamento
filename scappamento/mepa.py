# TODO: description header

from xlrd import open_workbook
from xlutils.copy import copy

from .supplier import Supplier, ScappamentoError


supplier_name = 'MEPA'


def update():
    # Config, filenames
    key_list = ['readypro_excel_filename',
                'mepa_excel_filename']
    mepa = Supplier(supplier_name, key_list)

    print(mepa)  # Title

    [readypro_excel_filename,
     mepa_excel_filename] = mepa.val_list

    # Copy data from generated spreadsheet to downloaded to-edit one
    readypro_xls = open_workbook(readypro_excel_filename)
    mepa_xls_model = open_workbook(mepa_excel_filename, formatting_info=True)

    mepa_xls_new = copy(mepa_xls_model)

    mepa_inst_sheet = mepa_xls_new.get_sheet(1)
    readypro_inst_sheet = readypro_xls.sheet_by_index(0)

    for i in range(1, 6):  # TODO: remove limits, test on file bounds
        for j in range(0, 20):
            mepa_inst_sheet.write(i, j, readypro_inst_sheet.cell_value(i, j))

    mepa_xls_new.save('C:\\Ready\\ReadyPro\\Archivi\\newmepatest.xls')  # TODO: actual final name and path


if __name__ == '__main__':
    update()
