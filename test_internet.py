import socket

def test():
    try:
        print('Checking for active internet...')
        socket.setdefaulttimeout(20)
        host = socket.gethostbyname('www.google.com')
        s = socket.create_connection((host,80), 2)
        s.close()
        return True
    except Exception as e:
        print(e)
    return False