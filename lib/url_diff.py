#!/usr/bin/env python3

import requests
import pickle
from email_alert import send_alert

default_cache = './temp/url_cache.bin'

class url_cache:
    #Request timeout in seconds
    timeout = 1
    def __init__(self):
        self.cache = {}

    #Takes a url and optional regex.  If the diff of the cached version with the latest version contains regex, return the HTML diff.  Otherwise return None.
    def url_diff(self, url, regex=''):
        try: 
            current_page = requests.get(url, timeout=url_cache.timeout)
            loaded_page = requests.get(url).text
            if current_page.text != loaded_page:
                return 'There was a diff'
            else:
                return None
        except:
            print('An exception occurred')
            return None

def main():
    #load cache
    try:
        cache_file = open(default_cache, 'rb')
        cache = pickle.load(cache_file)
        cache_file.close()
    except:
        cache = url_cache()

    while True:
        #query url
        url = input('Enter a url. Enter \'quit\' to exit: ')
        if url == 'quit':
            break

        #email and print results
        results = cache.url_diff(url)
        print(results)
        send_alert(results, ['ratherBrehearsin@yahoo.com'])

        
        #update the cache
        cache.cache[url] = results

    #write the cache
    cache_file = open(default_cache, 'wb')
    pickle.dump(cache,cache_file)
    cache_file.close()

if __name__ == '__main__':
    main()
