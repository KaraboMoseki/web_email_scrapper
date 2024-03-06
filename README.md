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
