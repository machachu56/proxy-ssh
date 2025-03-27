from utils.checker import checkProxies


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

