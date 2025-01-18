import re
import json
import requests
import urllib.request
from typing import Optional, List, TypedDict, Dict

# ~/.local/share/simsapa/api-port.txt
SIMSAPA_API_PORT = 4848

class VocabSection(TypedDict):
    title: str
    content: str
    deck_name: Optional[str]

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

def get_org_vocab_sections(content: str, keep_only_tag: Optional[str] = None) -> List[VocabSection]:
    # remove content up to the first second-level header (**)
    content = re.sub(r"^.*?(?=\n\*\* \w)", "\1", content, flags=re.DOTALL)

    def keep_section(s: str) -> bool:
        lines = s.split("\n")
        title = lines[0].strip()
        if ":noexport:" in title:
            return False
        if keep_only_tag and keep_only_tag in title:
            return True
        return False

    # split at sections, remove :noexport:, keep_only_tag
    sections = [i for i in content.split("\n** ") if keep_section(i)]

    vocab_sections: List[VocabSection] = []

    # .split() removes the sep string. First line is the heading, maybe with a tag.
    for i in sections:
        lines = i.split("\n")
        title = lines[0].strip()
        title = re.sub(r" +:[^:]+:", "", title)

        # :DECK_NAME: AN 10.81 Vāhanasutta
        m = re.search(r":DECK_NAME: +(.*)\n", i, flags=re.IGNORECASE)
        if m is None:
            deck_name = None
        else:
            deck_name = m.group(1)

        content = "\n".join(lines[1:])

        vocab_sections.append(VocabSection(
            title = title,
            content = content,
            deck_name = deck_name,
        ))

    return vocab_sections

def get_word_by_dpd_id(id: str) -> Dict[str, str]:
    resp = requests.get(f'http://localhost:{SIMSAPA_API_PORT}/words/{id}/dpd.json')
    if not resp.ok:
        raise Exception(resp)
    a = resp.json()
    return a[0]

def get_all_words_by_dpd_id(ids: List[str]) -> list:
    words = []
    for id in ids:
        w = get_word_by_dpd_id(id)
        words.append(w)
    return words

def normalize_sutta_ref(ref: str) -> str:
    flags = re.IGNORECASE

    # SN1.6 -> SN 1.6
    ref = re.sub(r'^([a-zA-Z]+)(\d)', r'\1 \2', ref, flags)

    ref = re.sub(r'ud *(\d)', r'Ud \1', ref, flags)
    ref = re.sub(r'uda *(\d)', r'Ud \1', ref, flags)
    ref = re.sub(r'khp *(\d)', r'Kp \1', ref, flags)
    ref = re.sub(r'th *(\d)', r'Thag \1', ref, flags)

    ref = ref.replace("SNP", "Snp")
    ref = ref.replace("DHP", "Dhp")
    ref = ref.replace("ITI", "Iti")
    ref = ref.replace("PV", "Pv")
    ref = ref.replace("VV", "Vv")
    ref = ref.replace("VISM", "Vism")
    ref = ref.replace("KP", "Kp")

    # PTS refs
    ref = re.sub(r'^d ', 'DN ', ref, flags)
    ref = re.sub(r'^m ', 'MN ', ref, flags)
    ref = re.sub(r'^s ', 'SN ', ref, flags)
    ref = re.sub(r'^a ', 'AN ', ref, flags)

    return ref.strip()
