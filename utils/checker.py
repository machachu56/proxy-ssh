import requests

def checkProxies(proxy, type, timeout):
    try:
        resp = requests.get("http://httpbin.org/get", proxies={type: proxy}, timeout=timeout).text
        if 'origin' in resp:
            print("Proxy working:", proxy)
            return type, proxy 
    except Exception as e:
        print("Proxy didn't work:", proxy, "| Error:", str(e))
    
    return None, None 
