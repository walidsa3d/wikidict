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

threads_result = {'mutable': None}


def get_summary(query, lang):
    url = "https://{lang}.wikipedia.org/w/api.php?continue=&action=query&titles={query}&prop=extracts&exintro=&explaintext=&format=json&redirects&formatversion=2".format(lang=lang, query=query)
    response = requests.get(url).json()
    pages = response['query']['pages']
    threads_result['mutable'] = pages[0].get('extract')
    return threads_result['mutable']


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
    parser.add_argument('-l', '--lang', help="wikipedia\'s language")
    args = parser.parse_args()
    lang = args.lang if args.lang in codes.keys() else 'en'
    query = ''.join(args.query).strip()
    worker = threading.Thread(
        name='worker', target=get_summary, args=(query, lang))
    worker.start()
    os.system('setterm -cursor off')
    # returns an infinite iterator
    spinner = itertools.cycle(["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"])
    while worker.isAlive():
        loading(spinner)
    terminal_width = os.popen('stty size', 'r').read().split()[1]
    text_width = 50*int(terminal_width)/100
    summary = colored(threads_result['mutable'], 'green', attrs=['bold'])
    if args.color:
        print textwrap.fill(summary, text_width, initial_indent='         ')
    else:
        print threads_result['mutable']
    os.system('setterm -cursor on')
