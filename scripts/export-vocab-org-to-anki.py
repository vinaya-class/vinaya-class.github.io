#!/usr/bin/env python3

import os
import sys
import re
from pathlib import Path
from helpers import anki_invoke, get_org_vocab_sections

def export_vocab(org_path: Path, apkg_path: Path, deck_name: str):
    with open(org_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = "\n".join([i['content'] for i in get_org_vocab_sections(content)])

    # Filter for three-column vocab table lines.
    # 1st col: English
    # 2nd col: Pali
    # 3rd col: 's' means this is a sentence
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

First argument: the path to the .org file, e.g. './vocabulary-lesson-1.org'.

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
