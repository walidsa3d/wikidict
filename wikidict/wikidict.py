#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .lancodes import codes
from sys import stdout
from termcolor import colored
import itertools
import threading
import os
import requests
import argparse
import textwrap
from time import sleep
import webbrowser


# Dummy client
class WikipediaClient(object):

    def __init__(self, query, lang):
        self.query = query
        self.lang = lang
        self.url = "https://{lang}.wikipedia.org/w/api.php?continue=&action=query&titles={query}&prop=extracts&exintro=&explaintext=&format=json&redirects&formatversion=2".format(lang=lang, query=query)

    def make_query(self):
        self.response = requests.get(self.url).json()

    def get_summary(self):
        pages = self.response['query']['pages']
        return pages[0].get('extract')

    def get_article_link(self):
        return "https://en.wikipedia.org/?curid={0}".format(self.response['query']['pages'][0].get('pageid'))


def loading(spinner):
    stdout.write('Getting the summary pal ')
    stdout.write(spinner.next())
    stdout.flush()
    stdout.write('\r')
    sleep(0.08)


def main():
    parser = argparse.ArgumentParser(usage="-h for full usage")
    parser.add_argument('query', help="search string", nargs="+")
    parser.add_argument('-c', '--color', action='store_true')
    parser.add_argument('-b', '--browser', action='store_true')
    parser.add_argument('-l', '--lang', help="wikipedia\'s language")
    args = parser.parse_args()
    lang = args.lang if args.lang in codes.keys() else 'en'
    query = ''.join(args.query).strip()

    # make a wikipedia client instance
    wd = WikipediaClient(query, lang)

    worker = threading.Thread(
        name='worker', target=wd.make_query)
    worker.start()
    os.system('setterm -cursor off')
    # returns an infinite iterator
    spinner = itertools.cycle(["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"])
    while worker.isAlive():
        loading(spinner)

    if args.browser:
        webbrowser.open(wd.get_article_link())
        os.system('setterm -cursor on')
        exit(0)
    terminal_width = os.popen('stty size', 'r').read().split()[1]
    text_width = 50*int(terminal_width)/100
    summary = colored(wd.get_summary(), 'green', attrs=['bold'])
    if args.color:
        print textwrap.fill(summary, text_width, initial_indent='         ')
    else:
        print wd.get_summary()
    os.system('setterm -cursor on')
