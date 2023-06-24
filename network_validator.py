from urllib import request

def has_connection_to_internet():
    try:
        request.urlopen('https://www.google.com', timeout=1)
        return True
    except request.URLError as err:
        return False
    