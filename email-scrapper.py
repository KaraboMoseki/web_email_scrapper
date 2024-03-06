from bs4 import BeautifulSoup
import requests
from requests.exceptions import MissingSchema, ConnectionError
import urllib.parse
from collections import deque
import re

user_url = str(input('[+] Enter target URL to scan: '))
urls = deque([user_url])

scraper_urls = set()
emails = set()

count = 0

try:
    while len(urls):
        count += 1
        if count == 100:
            break
        url = urls.popleft()
        scraper_urls.add(url)

        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)

        path = url[:url.rfind('/') + 1] if '/' in parts.path else url

        print('[%d] processing %s' % (count, url))
        try:
            response = requests.get(url)
        except (MissingSchema, ConnectionError):
            continue

        new_emails = set(re.findall(r'[a-z0-9\.\+_]+@[a-z0-9\.\-]+\.[a-z]+', response.text, re.I))
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, features='lxml')

        for anchor in soup.find_all("a"):
            link = anchor.get('href', '')
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            if link not in urls and link not in scraper_urls:
                urls.append(link)

except KeyboardInterrupt:
    print('[-] Closing!')

for mail in emails:
    print(mail)
        



