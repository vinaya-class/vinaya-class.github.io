#!/usr/bin/env python3

import os
import sys
import re
import json
import urllib.request
from pathlib import Path

def anki_request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def anki_invoke(action, params={}):
    request_json = json.dumps(anki_request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', request_json)))

    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')

    if 'error' not in response:
        raise Exception('response is missing required error field')

    if 'result' not in response:
        raise Exception('response is missing required result field')

    if response['error'] is not None:
        raise Exception(response['error'])

    return response['result']

def export_vocab(org_path: Path, apkg_path: Path, deck_name: str):
    with open(org_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # remove content up to the first second-level header (**)
    content = re.sub(r"^.*?(?=\n\*\* \w)", "\1", content, flags=re.DOTALL)

    # split at sections, filter :noexport:, re-join
    content = "\n".join([i for i in content.split("** ") if ":noexport:" not in i])

    # filter for three-column vocab table lines
    lines = [i for i in content.split("\n") if re.match(r"\|[^\|]+\|[^\|]+\|", i)]

    notes = []

    for i in lines:
        cols = [i.strip() for i in i.split("|")]

        # cols[0] is empty b/c of split on the the first "|"
        word = cols[1]
        meaning = cols[2]

        # Replace the markers {{  }} with <b> </b>
        example = cols[3].replace("{{", "<b>").replace("}}", "</b>")

        # Org-more /italics/
        pat_italic = re.compile(r"/\b([^/]+)\b/")
        pat_repl = "<i>\1</i>"

        word = pat_italic.sub(pat_repl, word)
        meaning = pat_italic.sub(pat_repl, meaning)
        example = pat_italic.sub(pat_repl, example)

        front = f"""
        <div style="font-size: 1.5em; padding: 1em;">{word}</div>
        <div style="font-size: 1em; padding: 1em;">{example}</div>
        """.strip().replace("\n", "")

        back = f"""<div style="font-size: 1em; padding: 1em;">{meaning}</div>"""

        notes.append({
            "deckName": deck_name,
            "modelName": "Basic",
            "fields": {"Front": front, "Back": back},
        })

    # If the deck exists, delete it. Ask the user for confirmation.

    if deck_name in anki_invoke('deckNames'):
        answer = input("The Anki deck exists. Delete it? [y/n]")
        if answer.lower() not in ["y", "yes"]:
            print("OK, not deleting the deck. Exiting.")
            sys.exit(2)

        anki_invoke("deleteDecks", params={"decks": [deck_name], "cardsToo": True})

    anki_invoke("createDeck", params={"deck": deck_name})

    anki_invoke("addNotes", params={"notes": notes})

    anki_invoke("exportPackage", params={"deck": deck_name, "path": os.path.abspath(str(apkg_path)), "includeSched": False})

if __name__ == "__main__":
    usage = """
Three arguments are expected:

First argument: the path to the .org file.

Second argument: the path to write the .apkg Anki Deck.

Third argument: the name of the Anki Deck.
"""

    if len(sys.argv) < 4:
        print(usage)
        sys.exit(2)

    org_path = Path(sys.argv[1])
    apkg_path = Path(sys.argv[2])
    deck_name = sys.argv[3]

    if org_path.exists():
        export_vocab(org_path, apkg_path, deck_name)

    else:
        print(f"File doesn't exist: {org_path}")
