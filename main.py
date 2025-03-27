import utils.scrape as scrape
import utils.utilities as utils
import utils.checker as checker
import concurrent.futures

goodProxies = []

threadsChecking = 50

# List of protocols to scrape
scrapeProtocols = ["http", "https", "socks4", "socks5"]

# Country
country = "US"

timeoutProxy = 5

if __name__ == '__main__':
    # Scrape
    protocolList = utils.parseProtocolsInput(scrapeProtocols)

    proxyList = scrape.runScrape(protocollist=protocolList, country=country)

    # Check the proxies
    for proxy in proxyList:
        protocol, ip, port = utils.separateIPPortProtocol(proxy)
        with concurrent.futures.ThreadPoolExecutor(max_workers=threadsChecking) as executor:
            results = executor.map(utils.check_proxy, [ip], [port], [protocol], [timeoutProxy])
            for result in results:
                if result != (None, None):
                    goodProxies.append(f"{result[0]}:{result[1]}")

    # Upload to server
    with open("proxies.txt", "w") as f:
        for proxy in goodProxies:
            f.write(proxy + "\n")

