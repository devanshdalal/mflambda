from diskcache import Cache


import requests
import urllib

cache = Cache(directory='.cache')
CACHE_VALIDITY = 3600 * 6  # 6 hours

def FetchPage(source):
	with Cache(cache.directory) as store:
		html = store.get(source)
		if not html:
			f = urllib.request.urlopen(source)
			html = f.read()
			store.set(source, html, expire=CACHE_VALIDITY)
		return html





