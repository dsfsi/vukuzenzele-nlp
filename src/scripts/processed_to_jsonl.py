import os, json, re
from pathlib import Path
from pprint import pprint
REPO_PATH = Path(os.path.abspath(__file__)).parent.parent.parent
DATA_PATH = Path(REPO_PATH / 'data')
PROCESSED_PATH = Path(DATA_PATH / 'processed')
OUT_PATH = Path(DATA_PATH / 'monolingual_jsonl')

languages = ['afr', 'eng', 'nbl', 'nso', 'sot', 'ssw', 'tsn', 'tso', 'ven', 'xho', 'zul']

def get_edition_paths():
    editions = os.listdir(PROCESSED_PATH)
    editions.remove('.gitkeep') # remove the .gitkeep
    editions.remove('.DS_Store') 
    editions.sort()
    return editions

def extract_text(txt_path):
    out = {}
    f = open(txt_path, 'r')
    text = ""
    for i,line in enumerate(f):
        if i == 0:
            out['title'] = line
        elif i == 1:
            continue
        elif i == 2:
            out['author'] = line
        elif i == 3:
            continue
        elif i > 4:
            text += line
    out['text'] = text
    return out

def write_to_jsonl(data, lang):
    out_path = Path(OUT_PATH / "{}.jsonl".format(lang))

    if os.path.exists(out_path):
        f = open(out_path,"a")
        f.write(json.dumps(data) + '\n')
    else:
        f = open(out_path,"w")
        f.write(json.dumps(data) + '\n')

    # print("'{}' converted to jsonl format".format(data['title']))

if __name__ == "__main__":
    editions = get_edition_paths()
    for edition in editions:
        edition_path = Path(PROCESSED_PATH / edition)
        txts = os.listdir(edition_path)
        for txt in txts:
            txt_path = Path(edition_path / txt)
            lang = re.search('afr|eng|nso|nbl|sot|ssw|tsn|tso|ven|xho|zul', txt).group() # what lang is it 
            out = extract_text(txt_path)
            out['edition'] = edition
            out['language_code'] = lang
            write_to_jsonl(out, lang)
            pprint(out)
            