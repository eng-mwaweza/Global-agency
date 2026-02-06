import requests

languages = ['', 'en', 'sw', 'ar', 'fr']
print('Testing language URLs:')
print('=' * 60)

for lang in languages:
    url = f'http://localhost:8000/{lang}/' if lang else 'http://localhost:8000/'
    try:
        r = requests.get(url, allow_redirects=True, timeout=5)
        final_url = r.url
        print(f'{lang if lang else "root":10s} -> Status {r.status_code:3d} | Final URL: {final_url}')
    except Exception as e:
        print(f'{lang if lang else "root":10s} -> Error: {str(e)[:40]}')
