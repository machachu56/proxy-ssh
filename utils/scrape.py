import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import utils.utilities as utilities
import subprocess


def extract_proxies(driver):
    """
    Extracts proxy entries from the current page.
    Each proxy is assumed to be in a table row with the IP in the first column (inside an <a> tag)
    and the port in the second column.
    """
    proxies = []
    try:
        # Wait until the table rows load (adjust the XPath if needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr"))
        )
    except Exception as e:
        print("Timeout or error waiting for table rows:", e)
        return proxies

    # Locate all rows in the table
    rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
    for row in rows:
        try:
            ip_element = row.find_element(By.XPATH, "./td[1]/a")
            port_element = row.find_element(By.XPATH, "./td[2]")
            protocol_element = row.find_element(By.XPATH, "./td[3]")
            ip = ip_element.text.strip()
            port = port_element.text.strip()
            protocol = protocol_element.text.strip().lower()
            
            proxies.append(f"{protocol}:{ip}:{port}")
        except Exception as e:
            print("Error extracting proxy from row:", e)
    return proxies

def click_next_page(driver):
    """
    Attempts to locate and click the "Next page" button.
    Returns True if successful, or False if the button is not found or cannot be clicked.
    """
    try:
        # Locate the button using its class and text
        next_button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-outline-secondary') and normalize-space(text())='Next page →']")
        
        if next_button.is_enabled():
            next_button.click()
            time.sleep(0.4)  # Adjust this if necessary
            return True
    except Exception as e:
        print("Next page button not found or error, DONE.")

    return False


def runScrape(protocollist, country):
    # Setup Selenium with headless Chrome
    subprocess.Popen("playwright install chromium")
    driver = uc.Chrome(headless=True,use_subprocess=False, browser_executable_path=utilities.get_chromium_path())
    url = f'https://www.proxydb.net/{protocollist}&country={country}'
    print(url)
    # Open ProxyDB.net
    driver.get(url=url)
    all_proxies = []

    # Loop through pages until there's no "Next page" button
    while True:
        proxies = extract_proxies(driver)
        all_proxies.extend(proxies)
        print(f"Scraped {len(proxies)} proxies from current page.")
        if not click_next_page(driver):
            print("No further pages. Exiting loop.")
            break

    driver.quit()

    unique_proxies = []
    seen_ips = set()

    for proxy in all_proxies:
        protocol, ip, port = utilities.separateIPPortProtocol(proxy)  # Extract IP from proxy
        if ip not in seen_ips:
            seen_ips.add(ip)
            unique_proxies.append(proxy)


    # Optionally, save the results to a file
    with open("proxies-nocheck.txt", "w") as f:
        for proxy in unique_proxies:
            f.write(proxy + "\n")
    print(f"Total proxies scraped: {len(all_proxies)}")
    print(f"Total unique proxies scraped: {len(unique_proxies)}")
    return unique_proxies
