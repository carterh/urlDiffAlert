#!/usr/bin/env python3

import requests

#Takes a url and optional regex.  If the diff of the cached version with the latest version contains regex, return the HTML diff.  Otherwise return None.
def url_diff(url, regex, cache_page):
    try: 
        loaded_page = requests.get(url, timeout=1).text
        if cache_page != loaded_page:
            return 'There was a diff for url: ' + url
        else:
            return None
    except BaseException as e:
        print(str(e))
        return None

def main():
    while True:
        #query url
        url = input('Enter a url. Enter \'quit\' to exit: ')
        if url == 'quit':
            break

        cache_page = requests.get(url, timeout=1).text
        results = url_diff(url, '', cache_page)
        print(results)

if __name__ == '__main__':
    main()
