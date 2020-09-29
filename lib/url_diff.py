#!/usr/bin/env python3

import requests
import difflib
import re

#Takes a url and optional regex.  If the diff of the cached version with the latest version contains regex, return the HTML diff.  Otherwise return None.
def url_diff(url, regex, cache_page, include_diff=False):
    try: 
        loaded_page = requests.get(url, timeout=1).text
        if cache_page != loaded_page:
            d = difflib.HtmlDiff()
            cache_lines = cache_page.splitlines()
            loaded_lines = loaded_page.splitlines()
            compact_diff = d.make_file(cache_lines, loaded_lines, context=True)
            if not re.search(regex, compact_diff):
                return None, loaded_page
            elif include_diff:
                return compact_diff, loaded_page
            else:
                return 'There was an update for: ' + url + ' : ' + regex, loaded_page
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
        results = url_diff(url, '.*', cache_page, include_diff=False)
        print(results[0])

if __name__ == '__main__':
    main()
