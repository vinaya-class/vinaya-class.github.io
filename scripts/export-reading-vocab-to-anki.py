#!/usr/bin/env python3

import os
import zipfile
import sys
import re
from pathlib import Path
from typing import TypedDict, Dict, List
from mako.template import Template

from helpers import anki_invoke, get_word_by_dpd_id, get_org_vocab_sections, normalize_sutta_ref

class NoteData(TypedDict):
    dpd_id: str # 40862
    word_json: Dict[str, str]
    reading_example: str
    reading_source: str

def export_vocab(org_path: Path):
    with open(org_path, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = get_org_vocab_sections(content, keep_only_tag=':anki:')

    deck_main = "Pāli Readings"

    with open(Path(__file__).parent.joinpath("anki_vocab_front.mako.html"), 'r', encoding="utf-8") as f:
        html_content = f.read()

    front_tmpl = Template(html_content)
    deck_files: List[Path] = []

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

                cloze_card = f""" <div style="line-height: 1.6; text-align: left; max-width: 52ex; padding: 1em; margin: 0 auto;">{cloze_text}</div> """

                anki_cloze_notes.append({
                    "deckName": deck_name,
                    "modelName": "Cloze",
                    "fields": {"Text": cloze_card},
                })

        # If the deck exists, delete it. Ask the user for confirmation.

        if deck_name in anki_invoke('deckNames'):
            answer = input(f"The Anki deck already exists: {deck_name}\nDelete it? [y/n]")
            if answer.lower() not in ["y", "yes"]:
                print("OK, not deleting the deck. Exiting.")
                sys.exit(2)
            else:
                print("Deleting deck.")

            anki_invoke("deleteDecks", params={"decks": [deck_name], "cardsToo": True})

        anki_invoke("createDeck", params={"deck": deck_name})

        anki_invoke("addNotes", params={"notes": anki_basic_notes})
        anki_invoke("addNotes", params={"notes": anki_cloze_notes})

        apkg_path = org_path.parent.joinpath(f"{reading_source}.apkg")

        anki_invoke("exportPackage", params={
            "deck": deck_main,
            "path": os.path.abspath(str(apkg_path)),
            "includeSched": False,
        })

        deck_files.append(apkg_path)

    zip_path = org_path.parent.joinpath("pali-readings-anki.zip")

    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        for file in deck_files:
            file_path = os.path.abspath(file)
            zip_file.write(file_path, arcname=os.path.basename(file))

    for i in deck_files:
        i.unlink()

if __name__ == "__main__":
    usage = f"""Usage:\n{Path(__file__).name} <pali-readings-next.org>"""

    if len(sys.argv) < 2:
        print(usage)
        sys.exit(2)

    org_path = Path(sys.argv[1])

    if org_path.exists():
        export_vocab(org_path)

    else:
        print(f"File doesn't exist: {org_path}")
