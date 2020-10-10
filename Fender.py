# --- Fender ---
# Read config file
# Log into website
# Download pre-made inventory Excel file
# Download custom-selected "specs" Excel file
# Convert both files to CSV

import os
import configparser
from requests import session
import chromedriver_binary  # Add ChromeDriver binary to path
from selenium import webdriver  # needs ChromeDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Event handler for specs_file watchdog
class FileCreationHandler(FileSystemEventHandler):
    # pass the observer to the handler, so that the former can be stopped by the latter
    def __init__(self, target_file, observer):
        self.target_file = target_file
        self.observer = observer
        self.found_file = ''

    def on_any_event(self, event):
        pass

    def on_created(self, event):
        if self.target_file in event.src_path and not event.src_path.endswith('.crdownload'):
            self.found_file = event.src_path  # annotate file
            self.observer.stop()  # stop watching

    def on_deleted(self, event):
        pass

    def on_modified(self, event):
        if self.target_file in event.src_path and not event.src_path.endswith('.crdownload'):
            self.found_file = event.src_path  # annotate file
            self.observer.stop()  # stop watching

    def on_moved(self, event):
        pass


def __main__():
    print('-- Fender --\n')

    # Credentials and URLs
    config = configparser.ConfigParser()
    with open('Fender.ini') as f:
        config.read_file(f)

        email = config['dealer.fender.com']['email']
        password = config['dealer.fender.com']['password']
        login_url = config['dealer.fender.com']['login_url']
        product_filtered_list_url = config['dealer.fender.com']['product_filtered_list_url']

        xlsx_inventory_filename = config['ReadyPro']['xlsx_inventory_filename']
        csv_inventory_filename = config['ReadyPro']['csv_inventory_filename']
        xlsx_specs_filename_partial = config['ReadyPro']['xlsx_specs_filename_partial']
        csv_specs_filename = config['ReadyPro']['csv_specs_filename']
        final_path = config['ReadyPro']['final_path']

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

        # Switch from Selenium to Requests, download inventory Excel file
        with session() as s:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                     "Chrome/44.0.2403.157 Safari/537.36 "
                       }
            s.headers.update(headers)
            for cookie in driver.get_cookies():
                c = {cookie['name']: cookie['value']}
                s.cookies.update(c)

            print('Downloading inventory...')
            r = s.get(excel_inventory_url)
            with open(final_path + xlsx_inventory_filename, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)

            # Back to Selenium, download specs Excel file
            print('Downloading specs...')
            driver.get(product_filtered_list_url)
            excel_dropdown_button = WebDriverWait(driver, timeout=4000) \
                .until(ec.element_to_be_clickable((By.ID, 'toggleDownloadsButton')))
            excel_dropdown_button.click()
            excel_specs_button = driver.find_element(By.ID, 'exportSpecsButton')
            excel_specs_button.click()

            # Poll directory where downloaded file will appear
            observer = Observer()
            event_handler = FileCreationHandler(xlsx_specs_filename_partial, observer)
            observer.schedule(event_handler, final_path, recursive=False)
            observer.start()
            observer.join()
            excel_specs_filename = event_handler.found_file  # absolute path, not just dir name

            # Logout
            logout_dropdown_button = driver.find_element(By.CLASS_NAME, 'dropdown-toggle')
            logout_dropdown_button.click()
            logout_button = driver.find_element(By.CSS_SELECTOR, '.dropdown-menu>li>a>i.fa-sign-out')
            logout_button.click()

    # Convert and save, delete original files
    inventory_list_xlsx = pd.read_excel(final_path + xlsx_inventory_filename, header=None)
    # TODO: add chromedriver to PATH (might be necessary on server as well)
    #  check header size and column names
    #  print(inventory_list_xlsx.columns)
    inventory_list_xlsx.to_csv(final_path + csv_inventory_filename, sep=';', header=None, index=False, encoding='utf-8')
    os.remove(final_path + xlsx_inventory_filename)

    specs_list_xlsx = pd.read_excel(excel_specs_filename, header=None)

    specs_list_xlsx.to_csv(final_path + csv_specs_filename, sep=';', header=None, index=False, encoding='utf-8')
    os.remove(excel_specs_filename)


if __name__ == '__main__':
    __main__()
