# TODO: description header

from .supplier import Supplier, ScappamentoError
from xlrd import open_workbook
from xlutils.copy import copy


def update():
    supplier_name = 'MEPA'
    mepa = Supplier(supplier_name)

    print(mepa)

    # Config
    config_path = 'C:\\Ready\\ReadyPro\\Archivi\\scappamento.ini'
    key_list = ['readypro_excel_filename',
                'mepa_excel_filename']

    mepa.load_config(key_list, config_path)

    [readypro_excel_filename,
     mepa_excel_filename] = mepa.val_list

    # Do stuff
    # xls = pd.read_excel(excel_filename, header=None)
    'Access||Accu Case||Acorn||ADAM Professional Audio'

    readypro_xls = open_workbook(readypro_excel_filename)
    mepa_xls_model = open_workbook(mepa_excel_filename, formatting_info=True)

    mepa_xls_new = copy(mepa_xls_model)

    mepa_inst_sheet = mepa_xls_new.get_sheet(1)
    readypro_inst_sheet = readypro_xls.sheet_by_index(0)

    for i in range(1, 6):  # TODO: remove limits, test on file bounds
        for j in range(0, 20):
            mepa_inst_sheet.write(i, j, readypro_inst_sheet.cell_value(i, j))

    mepa_xls_new.save('C:\\Ready\\ReadyPro\\Archivi\\newmepatest.xls')


if __name__ == '__main__':
    update()
