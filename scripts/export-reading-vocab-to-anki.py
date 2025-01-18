#!/usr/bin/env python3

import os
import zipfile
import sys
import re
from pathlib import Path
from typing import TypedDict, Dict, List
from mako.template import Template

from helpers import anki_invoke, get_word_by_dpd_id, get_org_vocab_sections, normalize_sutta_ref

DECK_MAIN = "Pāli Readings"

class NoteData(TypedDict):
    dpd_id: str # 40862
    word_json: Dict[str, str]
    reading_example: str
    reading_source: str

class DeckNotes(TypedDict):
    name: str
    notes: List[dict]

def create_export_decks_isolated(decks_notes: List[DeckNotes], export_dir: Path) -> List[Path]:
    # Change to the 'testing' profile.
    anki_invoke("loadProfile", params={"name": "testing"})

    deck_files: List[Path] = []

    for deck in decks_notes:
        print(deck["name"])

        # Delete any Pāli Readings decks before each iteration
        # to avoid duplicate cards from other suttas.
        anki_invoke("deleteDecks", params={"decks": [DECK_MAIN], "cardsToo": True})

        anki_invoke("createDeck", params={"deck": deck['name']})

        res = anki_invoke("canAddNotesWithErrorDetail", params={"notes": deck['notes']})
        for idx, i in enumerate(res):
            if not i['canAdd']:
                print(deck['notes'][idx])
                print(i['error'])

        anki_invoke("addNotes", params={"notes": deck['notes']})

        # Full deck name includes Pāli Readings::
        export_name = deck['name'].replace(f"{DECK_MAIN}::", "")

        apkg_path = export_dir.joinpath(f"{export_name}.apkg")

        anki_invoke("exportPackage", params={
            "deck": deck['name'],
            "path": os.path.abspath(str(apkg_path)),
            "includeSched": False,
        })

        deck_files.append(apkg_path)

    # Clean up
    anki_invoke("deleteDecks", params={"decks": [DECK_MAIN], "cardsToo": True})

    return deck_files

def zip_exported_decks(deck_files: List[Path]):
    zip_path = org_path.parent.joinpath("pali-readings-anki.zip")
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        for file in deck_files:
            file_path = os.path.abspath(file)
            zip_file.write(file_path, arcname=os.path.basename(file))

    for i in deck_files:
        i.unlink()

def export_vocab(org_path: Path):
    with open(org_path, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = get_org_vocab_sections(content, keep_only_tag=':anki:')

    with open(Path(__file__).parent.joinpath("anki_vocab_front.mako.html"), 'r', encoding="utf-8") as f:
        html_content = f.read()

    front_tmpl = Template(html_content)
    decks_notes: List[DeckNotes] = []
    deck_files: List[Path] = []

    for sec in sections:
        print(sec['title'])

        if sec["deck_name"]:
            reading_source = sec['deck_name']
        else:
            reading_source = sec['title']

        deck_name = f"{DECK_MAIN}::{reading_source}"

        # Extract DPD word id (40862/dpd -> 40862) from tables,
        # and the example sentence.

        # DPD ID to data
        vocab: Dict[str, NoteData] = {}

        anki_notes = []

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

            anki_notes.append({
                "deckName": deck_name,
                "modelName": "Basic (and reversed card)",
                "fields": {"Front": basic_front, "Back": basic_back},
            })

            if "<b>" in d["reading_example"]:
                cloze_text = d["reading_example"] \
                    .replace("<b>", "<b>{{c1::") \
                    .replace("</b>", "}}</b>")

                cloze_card = f""" <div style="line-height: 1.6; text-align: left; max-width: 52ex; padding: 1em; margin: 0 auto;">{cloze_text}</div> """

                anki_notes.append({
                    "deckName": deck_name,
                    "modelName": "Cloze",
                    "fields": {"Text": cloze_card},
                })

        decks_notes.append(DeckNotes(
            name = deck_name,
            notes = anki_notes,
        ))

    deck_files = create_export_decks_isolated(decks_notes, org_path.parent)

    zip_exported_decks(deck_files)

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
