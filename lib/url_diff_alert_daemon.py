#!/usr/bin/env python3

from url_diff import url_diff
import json
import pickle
from collections import defaultdict
from time import sleep
from email_alert import send_alert

class config:
    def __init__(self, rules, recipients):
        self.rules = rules
        self.recipients = recipients
        self.check_interval = 5*60

    @staticmethod
    def load_config(path):
        config_file = open(path)
        config_map = json.load(config_file)
        config_file.close()
        return config(config_map['rules'], config_map['recipients'])

default_cache = './temp/url_cache.bin'
default_config = './config.json'

class url_cache:
    def __init__(self):
        self.cache = defaultdict(str)

class daemon:
    def __init__(self, config, state):
        self.config = config
        self.state = state

    def start(self):
        print('Starting daemon')
        while True:
            for rule in self.config.rules:
                url = rule['url']
                regex = rule['regex']
                try:
                    result = url_diff(rule['url'], rule['regex'], self.state.cache[(url,regex)])
                    if result:
                        print('New result for ' + url + ' , emailing')
                        send_alert(result[0], self.config.recipients)
                        self.state.cache[(url,regex)] = result[1]
                except BaseException as e:
                    print(str(e))
            
            #write the cache, sleep
            print('Writing cache')
            try:
                cache_file = open(default_cache, 'wb')
                pickle.dump(self.state,cache_file)
                cache_file.close()
            except BaseException as e:
                print(str(e))
            sleep(self.config.check_interval)

def main():
    conf = config.load_config(default_config) 

    try:
        cache_file = open(default_cache, 'rb')
        cache = pickle.load(cache_file)
        cache_file.close()
    except:
        cache = url_cache()

    proc = daemon(conf, cache)
    proc.start()

if __name__ == '__main__':
    main()
