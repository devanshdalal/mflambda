import os

CACHE_REQUESTS = "CACHE_REQUESTS" in os.environ
print('CACHE_REQUESTS', CACHE_REQUESTS)

cache = None
if CACHE_REQUESTS:
	from diskcache import Cache
	cache = Cache(directory='/tmp/.cache')
	CACHE_VALIDITY = 3600 * 6  # 6 hours

import requests
import urllib


def FetchPage(source):
	if CACHE_REQUESTS:
		with Cache(cache.directory) as store:
			html = store.get(source)
			if not html:
				f = urllib.request.urlopen(source)
				html = f.read()
				store.set(source, html, expire=CACHE_VALIDITY)
			return html
	else:
		f = urllib.request.urlopen(source)
		return f.read()





