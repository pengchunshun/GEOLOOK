import urllib.request as u, socket, time
ip = '14.155.53.35'
port = 8899
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
try:
    s.connect((ip, port))
    print('PUBLIC PORT 8899 OPEN')
    s.close()
except Exception as e:
    print('PUBLIC PORT 8899 CLOSED:', e)

# also try fetch
for scheme in ['http://', 'https://']:
    try:
        url = scheme + ip + ':8899/'
        r = u.urlopen(url, timeout=8)
        print(url, '->', r.status)
    except Exception as e:
        print(url, '-> ERR', str(e)[:100])
