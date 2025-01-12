#!/usr/bin/env python3

import os
import sys
import re
from pathlib import Path
from typing import TypedDict, Dict
from mako.template import Template

from helpers import anki_invoke, get_word_by_dpd_id, get_org_vocab_sections, normalize_sutta_ref

class NoteData(TypedDict):
    dpd_id: str # 40862
    word_json: Dict[str, str]
    reading_example: str
    reading_source: str

def export_vocab(org_path: Path, apkg_path: Path):
    with open(org_path, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = get_org_vocab_sections(content, keep_only_tag=':anki:')

    deck_main = "Pāli Readings"

    with open(Path(__file__).parent.joinpath("anki_vocab_front.mako.html"), 'r', encoding="utf-8") as f:
        html_content = f.read()

    front_tmpl = Template(html_content)

    for sec in sections:
        if sec["deck_name"]:
            deck_name = f"{deck_main}::{sec['deck_name']}"
            reading_source = sec['deck_name']
        else:
            deck_name = f"{deck_main}::{sec['title']}"
            reading_source = sec['title']

        # Extract DPD word id (40862/dpd -> 40862) from tables,
        # and the example sentence.

        # DPD ID to data
        vocab: Dict[str, NoteData] = {}

        for line in sec['content'].split("\n"):
            m = re.search(r"\| *([0-9]+)/dpd *\|([^\|]+)\|", line)
            if m is None:
                continue
            else:
                dpd_id = m.group(1)

                # Replace the markers {{  }} with <b> </b>
                reading_example = m.group(2).replace("{{", "<b>").replace("}}", "</b>")

                if dpd_id not in vocab.keys():
                    vocab[dpd_id] = NoteData(
                        dpd_id = dpd_id,
                        word_json = get_word_by_dpd_id(dpd_id),
                        reading_example = reading_example,
                        reading_source = reading_source,
                    )
                else:
                    raise Exception(f"Duplicate: {dpd_id}")

        anki_basic_notes = []
        anki_cloze_notes = []

        for d in vocab.values():
            basic_front = front_tmpl.render(
                d = d,
                w = d["word_json"],
                normalize_sutta_ref = normalize_sutta_ref,
            )

            meaning = d["word_json"]["meaning_1"]
            if d["word_json"]["meaning_lit"] != "":
               meaning = meaning.strip() + "; lit. " + d["word_json"]["meaning_lit"]

            basic_back = f"""<div style="font-size: 1em; padding: 1em;">{meaning}</div>"""

            anki_basic_notes.append({
                "deckName": deck_name,
                "modelName": "Basic (and reversed card)",
                "fields": {"Front": basic_front, "Back": basic_back},
            })

            if "<b>" in d["reading_example"]:
                cloze_text = d["reading_example"] \
                    .replace("<b>", "<b>{{c1::") \
                    .replace("</b>", "}}</b>")

                anki_cloze_notes.append({
                    "deckName": deck_name,
                    "modelName": "Cloze",
                    "fields": {"Text": cloze_text},
                })

        # If the deck exists, delete it. Ask the user for confirmation.

        if deck_name in anki_invoke('deckNames'):
            answer = input("The Anki deck exists. Delete it? [y/n] ")
            if answer.lower() not in ["y", "yes"]:
                print("OK, not deleting the deck. Exiting.")
                sys.exit(2)

            anki_invoke("deleteDecks", params={"decks": [deck_name], "cardsToo": True})

        anki_invoke("createDeck", params={"deck": deck_name})

        anki_invoke("addNotes", params={"notes": anki_basic_notes})
        anki_invoke("addNotes", params={"notes": anki_cloze_notes})

    anki_invoke("exportPackage", params={
        "deck": deck_main,
        "path": os.path.abspath(str(apkg_path)),
        "includeSched": False,
    })

if __name__ == "__main__":
    usage = f"""Usage:\n{Path(__file__).name} <pali-readings-next.org> [pali-readings-next.apkg]"""

    if len(sys.argv) < 2:
        print(usage)
        sys.exit(2)

    org_path = Path(sys.argv[1])
    if len(sys.argv) > 2:
        apkg_path = Path(sys.argv[2])
    else:
        apkg_path = org_path.with_suffix(".apkg")

    if org_path.exists():
        export_vocab(org_path, apkg_path)

    else:
        print(f"File doesn't exist: {org_path}")
