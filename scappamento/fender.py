# --- Fender ---
# Read config file
# Log into B2B website
# Download pre-made inventory Excel file (no disk)
# Download custom-selected "specs" Excel file (no disk)
# Convert both files to CSV

# from .supplier import Supplier, ScappamentoError TODO: when script will be imported, not executed
import scappamento.supplier
from requests import session
import chromedriver_binary  # Add ChromeDriver binary to path
from selenium import webdriver  # needs ChromeDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pandas as pd


def __main__():
    supplier_name = 'Fender'
    fender = scappamento.supplier.Supplier(supplier_name)

    print(fender)

    # Credentials and URLs
    key_list = ['email',
                'password',
                'login_url',
                'xlsx_specs_url',
                'csv_inventory_filename',
                'csv_specs_filename',
                'final_path']

    config_path = 'C:\\Ready\\ReadyPro\\Archivi\\scappamento.ini'

    fender.load_config(key_list, config_path)

    [email,
     password,
     login_url,
     xlsx_specs_url,
     csv_inventory_filename,
     csv_specs_filename,
     final_path] = fender.val_list

    chromedriver_path = chromedriver_binary.chromedriver_filename
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': final_path,
             'download.prompt_for_download': False,
             'download.directory_upgrade': True}
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--headless')
    with webdriver.Chrome(options=options) as driver:
        # Login
        print('ChromeDriver path:', chromedriver_path, '\n\nLogging in...')
        driver.get(login_url)

        email_input = driver.find_element(By.ID, 'emailInput')
        email_input.send_keys(email)

        pass_input = driver.find_element(By.ID, 'passwordInput')
        pass_input.send_keys(password)

        login_butt = driver.find_element(By.ID, 'submitLoginButton')
        login_butt.click()

        excel_inventory_button = WebDriverWait(driver, timeout=4000) \
            .until(ec.element_to_be_clickable((By.ID, 'inventoryDownloadButton')))
        excel_inventory_url = excel_inventory_button.get_attribute('href')

        # Switch from Selenium to Requests
        with session() as s:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 "
                              "(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36 "
                       }
            s.headers.update(headers)
            for cookie in driver.get_cookies():  # port session cookies over
                c = {cookie['name']: cookie['value']}
                s.cookies.update(c)

            print('Downloading inventory...')
            r_inventory = s.get(excel_inventory_url)  # download inventory Excel file

            print('Downloading specs...')
            r_specs = s.get(xlsx_specs_url)  # download specs Excel file

            # Logout (Selenium)
            logout_dropdown_button = driver.find_element(By.CLASS_NAME, 'dropdown-toggle')
            logout_dropdown_button.click()
            logout_button = driver.find_element(By.CSS_SELECTOR, '.dropdown-menu>li>a>i.fa-sign-out')
            logout_button.click()

    # Convert to CSV and save
    # TODO: check header size and column names
    inventory_list_xlsx = pd.read_excel(r_inventory.content, header=None)
    inventory_list_xlsx.to_csv(final_path + csv_inventory_filename, sep=';', header=None, index=False)

    specs_list_xlsx = pd.read_excel(r_specs.content, header=None)
    specs_list_xlsx.to_csv(final_path + csv_specs_filename, sep=';', header=None, index=False)


if __name__ == '__main__':
    __main__()
