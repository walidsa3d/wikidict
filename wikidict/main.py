import click
import requests
import itertools
import threading
import os
import textwrap
from rich.console import Console
from rich.spinner import Spinner
from rich.text import Text
from wikidict.lancodes import codes

console = Console()

class Info:
    SUMMARY = "Not Found"

def get_summary(query, lang):
    url = f"https://{lang}.wikipedia.org/w/api.php?continue=&action=query&titles={query}&prop=extracts&exintro=&explaintext=&format=json&redirects&formatversion=2"
    response = requests.get(url).json()
    pages = response['query']['pages']
    extract = pages[0].get('extract', None)
    if extract is not None:
        Info.SUMMARY = extract

def justify_text(text, width):
    words = text.split()
    lines = []
    line = []
    line_length = 0
    for word in words:
        if line_length + len(word) + len(line) <= width:
            line.append(word)
            line_length += len(word)
        else:
            if line:
                spaces_to_add = width - line_length
                spaces_between_words = len(line) - 1
                if spaces_between_words > 0:
                    space_per_gap = spaces_to_add // spaces_between_words
                    extra_spaces = spaces_to_add % spaces_between_words
                    justified_line = ''
                    for i, word in enumerate(line):
                        justified_line += word
                        if i < spaces_between_words:
                            justified_line += ' ' * (space_per_gap + (1 if i < extra_spaces else 0))
                    lines.append(justified_line)
                else:
                    lines.append(line[0])
            line = [word]
            line_length = len(word)
    if line:
        lines.append(' '.join(line))  # Last line is left-aligned
    return '\n'.join(lines)

@click.command()
@click.argument('query', nargs=-1)
@click.option('--lang', '-l', default='en', help="Wikipedia's language code")
@click.option('--color/--no-color', default=True, help="Enable or disable colored output")
def main(query, lang, color):
    if lang not in codes.keys():
        lang = 'en'
    query = ' '.join(query).strip()

    # Start a spinner thread while loading
    worker = threading.Thread(target=get_summary, args=(query, lang))
    worker.start()

    # Create a spinner using rich
    spinner = Spinner('dots', text='Fetching summary...')
    with console.status(spinner, spinner_style="green") as status:
        while worker.is_alive():
            worker.join(0.1)  # Ensure we don't hang the main thread

    # Summary has been fetched
    terminal_width = os.get_terminal_size().columns
    text_width = int(0.8 * terminal_width)  # 80% of terminal width
    summary_text = Info.SUMMARY

    # Justify the text
    justified_summary = justify_text(summary_text, text_width)

    if color:
        justified_summary = Text(justified_summary, style="bold green")

    # Print the result with rich
    console.print(justified_summary)

if __name__ == "__main__":
    main()