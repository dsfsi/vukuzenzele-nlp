import os, json, re
from pathlib import Path
from pprint import pprint
REPO_PATH = Path(os.path.abspath(__file__)).parent.parent.parent
DATA_PATH = Path(REPO_PATH / 'data')
PROCESSED_PATH = Path(DATA_PATH / 'processed')
OUT_PATH = Path(DATA_PATH / 'editions_json')

languages = ['afr', 'eng', 'nbl', 'nso', 'sot', 'ssw', 'tsn', 'tso', 'ven', 'xho', 'zul']

def fetch_data_edition_filepaths(): # -> list[str]
    all_paths = os.listdir(PROCESSED_PATH) # list the directories in /data/processed
    all_paths.remove('.gitkeep') # remove the .gitkeep
    try: all_paths.remove('.DS_Store') 
    except: pass # remove the .DS
    all_paths.sort() # sort them

    return all_paths

def fetch_data_txt_filepaths(edition):
    txt_paths = os.listdir('{}/{}'.format(PROCESSED_PATH, edition)) 
    return txt_paths

def build_filepaths_dictonary():
    filepaths_dictionary = {} 
    edition_paths = fetch_data_edition_filepaths() 
    for edition in edition_paths:
        txt_paths = fetch_data_txt_filepaths(edition) 
        for txt in txt_paths: 
            lang = re.search('afr|eng|nso|nbl|sot|ssw|tsn|tso|ven|xho|zul', txt).group() 
            story_no = re.search('\d{2}',txt[7:]).group()
            
            if edition not in filepaths_dictionary.keys():
                filepaths_dictionary[edition] = {story_no : {lang : txt}}
            elif story_no not in filepaths_dictionary[edition].keys(): 
                filepaths_dictionary[edition][story_no] = {lang : txt} 
            else: 
                filepaths_dictionary[edition][story_no][lang] = txt 
                

    return filepaths_dictionary 



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

def write_to_json(data):
    if not os.path.exists(OUT_PATH):
        os.makedirs(OUT_PATH)

    f = open(OUT_PATH / 'vukuzenzele.json', 'w')
    json.dump(data, f)


if __name__ == "__main__":
    file_paths = build_filepaths_dictonary()
    out_list = []
    # pprint(file_paths)
    for edition_key in file_paths.keys():
        edition = file_paths[edition_key]
        for story_no in edition:
            print(edition_key, story_no)
            out = {
                'edition' : edition_key,
                'article_no' : story_no,
            }
            
            for lang_key in edition[story_no].keys():
                text_path = edition[story_no][lang_key]
                data = extract_text(Path(PROCESSED_PATH / edition_key / text_path))
                out[lang_key] = data
            out_list.append(out)
    write_to_json(out_list)