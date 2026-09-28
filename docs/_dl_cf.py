import urllib.request as u, os, sys

mirrors = [
    'https://mirror.ghproxy.com/https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe',
    'https://gh.api.99988866.xyz/https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe',
    'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe',
]
out = r'g:\AI_SPACE\CodeBuddy\geolook\docs\cloudflared.exe'
if os.path.exists(out):
    print('exists', os.path.getsize(out))
    sys.exit(0)
for url in mirrors:
    print('try', url[:60])
    try:
        u.urlretrieve(url, out)
        print('done', os.path.getsize(out))
        sys.exit(0)
    except Exception as e:
        print('err', e)
print('all failed')
