from utils.checker import checkProxies
import os
import glob
import platform

def parseProtocolsInput(protocols):
    query_list = []

    for i, protocol in enumerate(protocols):
        prefix = "?protocol=" if i == 0 else "&protocol="
        query_list.append(f"{prefix}{protocol}")

    query_string = "".join(query_list)
    return query_string

def separateIPPortProtocol(proxy):
    protocol = proxy.split(':')[0]
    ip = proxy.split(':')[1]
    port = proxy.split(':')[2]

    return protocol, ip, port


def check_proxy(ip, port, protocol, timeout=5):
    return checkProxies(f"{ip}:{port}", protocol, timeout)

def get_chromium_path():
    # Determine the base path depending on the operating system
    if platform.system() == 'Windows':
        ms_playwright_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'ms-playwright')
        chromium_folders = glob.glob(os.path.join(ms_playwright_path, 'chromium-*'))
        
        if chromium_folders:
            chromium_path = chromium_folders[0]  # Latest Chromium version
            chrome_executable = os.path.join(chromium_path, 'chrome-win', 'chrome.exe')
            return chrome_executable
        else:
            raise FileNotFoundError("Chromium folder not found on Windows.")

    elif platform.system() == 'Linux':
        ms_playwright_path = os.path.join(os.environ['HOME'], '.cache', 'ms-playwright')
        chromium_folders = glob.glob(os.path.join(ms_playwright_path, 'chromium-*'))
        
        if chromium_folders:
            chromium_path = chromium_folders[0]  # Latest Chromium version
            chrome_executable = os.path.join(chromium_path, 'chrome-linux', 'chrome')
            return chrome_executable
        else:
            raise FileNotFoundError("Chromium folder not found on Linux.")
    else:
        raise OSError("Unsupported OS")


