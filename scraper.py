from chromedriver_py import binary_path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os
import openpyxl

# Declare variables outside try block
input_file = None
driver = None
data_file = None

try:
    # Check if the input file exists
    input_file_path = 'input.txt'
    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"Input file '{input_file_path}' not found.")

    # Handling Input file
    input_file = open('input.txt', 'r', encoding='utf-8')
    lines = input_file.readlines()
    addresses = [line.strip() for line in lines]

    # Creating Excel file to save the data
    data_file = 'GMap_data.xlsx'
    if os.path.exists(data_file):
        workbook = openpyxl.load_workbook(data_file)
        sheet = workbook.active
    else:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(['Address', 'Name', 'Contact'])

    url = "https://www.google.com/maps/@31.506432,74.3243776,12z?entry=ttu"


    def create_driver(url = url):
        # SETTING THE CHROME BROWSER
        chrome_options = Options()
        chrome_options.add_argument('--window')  # Enable windowed mode
        # Set up ChromeService
        svc = webdriver.ChromeService(executable_path=binary_path)
        # Create a WebDriver instance with the specified options and service
        driver = webdriver.Chrome(service=svc, options=chrome_options)
        wait = WebDriverWait(driver, 60)
        # Entering the visit
        driver.get(url=url)
        return driver, wait


    driver, wait = create_driver()
    max_attempts = 2
    index = 0
    for address in addresses:
        time.sleep(1)
        print(f"-------------------------{index}--------------------------")
        attempts = 0
        while attempts < max_attempts:
            try:
                time.sleep(2)
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[id="searchbox"] input')))
                search_bar = driver.find_element(By.CSS_SELECTOR, 'div[id="searchbox"] input')
                search_bar.clear()
                time.sleep(1)
                search_bar.send_keys(address)
                search_bar.send_keys(Keys.RETURN)
                print(f"Address visited: {address}"
                # GETTING INSIDE THE ENTRY FIRST WE WILL WAIT FOR CONTACT INFO (WHETHER IT'S THERE OR NOT) JUST TO MAKE SURE PAGE GETS LOADED COMPLETELY
                try:
                    WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, 'button[data-tooltip="Copy phone number"]')))  # Click the view all btn
                except (TimeoutException, NoSuchElementException):
                    pass

                # added----
                try:
                    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.TAG_NAME, 'h1')))
                    time.sleep(2)
                    name = driver.find_element(By.TAG_NAME, 'h1').text
                except (TimeoutException, NoSuchElementException):
                    print(f"Partial Address : {address}")
                    try:
                        WebDriverWait(driver, 3).until(
                            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class^="Nv2PK"]')))

                        unmatched_entities = driver.find_elements(By.CSS_SELECTOR, 'div[class^="Nv2PK"]')
                        for entity in range(len(unmatched_entities)):
                            unmatched_entities = driver.find_elements(By.CSS_SELECTOR, 'div[class^="Nv2PK"]')
                            element = unmatched_entities[entity]
                            driver.execute_script("arguments[0].scrollIntoView();", element)
                            element.find_element(By.CSS_SELECTOR, 'a[class="hfpxzc"]').click()
                            # added----
                            try:
                                wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'h1')))
                                time.sleep(2)
                                name = driver.find_element(By.TAG_NAME, 'h1').text
                            except (NoSuchElementException, NoSuchElementException):
                                continue
                            time.sleep(1)  # 2nd add
                            try:

                                contact = driver.find_element(By.CSS_SELECTOR,
                                                              'button[data-tooltip="Copy phone number"]').get_attribute(
                                    'aria-label').strip('Phone:').strip()
                            except NoSuchElementException:
                                contact = None

                            print(f"Name (unmatched) : {name}")
                            print(f"Contact (unmatched) : {contact}")
                            sheet.append([address, name, contact])
                            workbook.save(data_file)
                            time.sleep(2)
                            # ----- added
                            initial_url = driver.current_url
                            driver.execute_script("window.history.go(-1)")
                            time.sleep(2)
                            post_url = driver.current_url
                            if initial_url == post_url:
                                driver.execute_script("window.history.go(-1)")
                    except (TimeoutException, NoSuchElementException):
                        pass
                    print("partial matched part ended...")
                    break
                time.sleep(1)  # 2nd add
                # CHECKING IF THE ENTRY HAS ANY CONTACT IF NOT IT WILL SIMPLY MAKE IT NULL
                try:
                    contact = driver.find_element(By.CSS_SELECTOR,
                                                  'button[data-tooltip="Copy phone number"]').get_attribute(
                        'aria-label').strip('Phone:').strip()
                except NoSuchElementException:
                    contact = None

                print(f"Name : {name}")
                print(f"Contact : {contact}")
                sheet.append([address, name, contact])
                workbook.save(data_file)

                # HERE WE WILL LOOK IF THERE ARE MORE ENTRIES BY CHECKING IF IT HAS 'VIEW ALL' BUTTON
                try:
                    view_all_btn = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="View all"] span')
                except NoSuchElementException:
                    view_all_btn = None

                try:
                    WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class^="Nv2PK"]')))
                    no_btn_element = driver.find_elements(By.CSS_SELECTOR, 'div[class^="Nv2PK"]')
                except (NoSuchElementException, TimeoutException):
                    no_btn_element = None
                if view_all_btn is None and no_btn_element is not None:
                    print("view_all_btn is None and no_btn_element is not None")
                    no_btn_element = driver.find_elements(By.CSS_SELECTOR, 'div[class^="Nv2PK"]')
                    for element in range(len(no_btn_element)):
                        no_btn_element = driver.find_elements(By.CSS_SELECTOR, 'div[class^="Nv2PK"]')
                        driver.execute_script("arguments[0].scrollIntoView();", no_btn_element[element])
                        no_btn_element[element].find_element(By.CSS_SELECTOR, 'button[class="hfpxzc"]').click()
                        # added----
                        try:
                            # time.sleep(1)
                            wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'h1')))
                            time.sleep(2)
                            name = driver.find_element(By.TAG_NAME, 'h1').text
                        except NoSuchElementException:
                            continue
                        time.sleep(1)
                        try:
                            contact = driver.find_element(By.CSS_SELECTOR,
                                                          'button[data-tooltip="Copy phone number"]').get_attribute(
                                'aria-label').strip('Phone:').strip()
                        except NoSuchElementException:
                            contact = None

                        print(f"Name : {name}")
                        print(f"Contact : {contact}")
                        sheet.append([address, name, contact])
                        workbook.save(data_file)
                        time.sleep(2)
                        # ----- added
                        initial_url = driver.current_url
                        driver.execute_script("window.history.go(-1)")
                        time.sleep(3)
                        post_url = driver.current_url

                        if initial_url == post_url:
                            driver.execute_script("window.history.go(-1)")

                        try:
                            WebDriverWait(driver, 2).until(
                                EC.visibility_of_element_located(
                                    (By.CSS_SELECTOR, 'div[class^="Nv2PK"]')))
                        except (TimeoutException, NoSuchElementException):
                            # continue
                            pass
                    break
                # IF THE BUTTON IS NOT THEN IT WILL PROCEED TO GET THE FURTHER ENTRIES ELSE IT WILL SKIP
                if view_all_btn is not None:
                    print("view_all_btn is not None")
                    # Scroll to the button
                    driver.execute_script("arguments[0].scrollIntoView();", view_all_btn)
                    time.sleep(2)
                    view_all_btn.click()
                    time.sleep(1)
                    # After clicking checking for the further entries
                    # ----- added
                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class^="Nv2PK"]')))

                    # Here we will grab the entries
                    previous_count = len(driver.find_elements(By.CSS_SELECTOR, 'div[class^="Nv2PK"]'))
                    print(f"Total Entries: {previous_count}")
                    while True:
                        elements = driver.find_elements(By.CSS_SELECTOR, 'div[class^="Nv2PK"]')
                        last_element = elements[-1]
                        driver.execute_script("arguments[0].scrollIntoView();", last_element)
                        time.sleep(2)
                        driver.execute_script("arguments[0].scrollIntoView();", last_element)
                        time.sleep(3)
                        current_count = len(driver.find_elements(By.CSS_SELECTOR, 'div[class^="Nv2PK"]'))
                        print(f"prev : {previous_count}, current:{current_count}")
                        if current_count == previous_count:
                            break
                        previous_count = current_count

                    total_links = current_count

                    # Looping through all entries
                    for link in range(total_links):
                        try:
                            print(f"Entry No. : {link}")
                            # waiting for the entries to show again to avoid stale element exception
                            try:
                                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class^="Nv2PK"]')))
                            except TimeoutException:
                                time.sleep(3)
                                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class^="Nv2PK"]')))
                            # ------------------------------------#
                            # Here we will grab the entries
                            while True:
                                elements = driver.find_elements(By.CSS_SELECTOR, 'div[class^="Nv2PK"]')
                                last_element = elements[-1]
                                driver.execute_script("arguments[0].scrollIntoView();", last_element)
                                time.sleep(2)
                                driver.execute_script("arguments[0].scrollIntoView();", last_element)
                                time.sleep(3)
                                current_count = len(driver.find_elements(By.CSS_SELECTOR, 'div[class^="Nv2PK"]'))
                                print(f"prev : {previous_count}, current:{current_count}")
                                if current_count == previous_count:
                                    break
                                previous_count = current_count

                            entries_links = driver.find_elements(By.CSS_SELECTOR, 'div[class^="Nv2PK"]')
                            driver.execute_script("arguments[0].scrollIntoView();", entries_links[link])
                            entries_links[link].find_element(By.CSS_SELECTOR, 'button[class="hfpxzc"]').click()

                            time.sleep(2)  # added extra wait
                            try:
                                WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
                                    (
                                        By.CSS_SELECTOR,
                                        'button[data-tooltip="Copy phone number"]')))  # Click the view all btn
                            except TimeoutException:
                                pass
                            # added----
                            try:
                                wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'h1')))
                                time.sleep(2)
                                name = driver.find_element(By.TAG_NAME, 'h1').text
                            except NoSuchElementException:
                                continue
                            time.sleep(1)  # 2nd add
                            try:
                                contact = driver.find_element(By.CSS_SELECTOR,
                                                              'button[data-tooltip="Copy phone number"]').get_attribute(
                                    'aria-label').strip('Phone:').strip()
                            except NoSuchElementException:
                                contact = None
                            time.sleep(1)  # 2nd add
                            print(f"Name : {name}")
                            print(f"Contact : {contact}")
                            sheet.append([address, name, contact])
                            workbook.save(data_file)
                            time.sleep(2)
                            # ----- added
                            initial_url = driver.current_url
                            driver.execute_script("window.history.go(-1)")
                            time.sleep(2)
                            post_url = driver.current_url
                            if initial_url == post_url:
                                driver.execute_script("window.history.go(-1)")
                            # Here it will see if it has hit the back button twice
                            try:
                                WebDriverWait(driver, 2).until(
                                    EC.visibility_of_element_located(
                                        (By.CSS_SELECTOR, 'button[aria-label="View all"] span')))
                            except (TimeoutException, NoSuchElementException):
                                continue
                            # Click the view all btn
                            view_all_btn = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="View all"] span')
                            driver.execute_script("arguments[0].scrollIntoView();", view_all_btn)
                            time.sleep(3)
                            view_all_btn.click()
                            print("---------------------------------")

                        except (
                                TimeoutException, NoSuchElementException,
                                StaleElementReferenceException):  # added for inner loop
                            continue
                break  # added to break while

            except Exception as e:
                print(f"Exception occurred: {e}")
                print(f"{attempts} attempt on {address}")
                attempts += 1

        else:
            continue

        index += 1
        if index % 300 == 0:
            print("Killing the Chrome Session.")
            driver.quit()
            time.sleep(10)
            print("Creating new Chrome Driver.")
            driver, wait = create_driver()
except KeyboardInterrupt:
    print("Keyboard interrupt detected, exiting gracefully.")
    input_file.close()
    driver.quit()
