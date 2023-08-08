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

def fetch_data_txt_filepaths(edition): # -> list[str]
    txt_paths = os.listdir('{}/{}'.format(PROCESSED_PATH, edition)) # list the directories in /data/processed/edition
    return txt_paths

def build_filepaths_dictonary():
    filepaths_dictionary = {} # empty dict to append to
    edition_paths = fetch_data_edition_filepaths() # build edition keys
    for edition in edition_paths: # for each edition
        txt_paths = fetch_data_txt_filepaths(edition) # list of txt paths inside an edition dir
        for txt in txt_paths: #for each txt file
            lang = re.search('afr|eng|nso|nbl|sot|ssw|tsn|tso|ven|xho|zul', txt).group() # what lang is it 
            if edition not in filepaths_dictionary.keys(): # if edition is not present in dict
                filepaths_dictionary[edition] = {lang : [txt]} # create end : { 2020-01-ed1 : [eng-01.txt, eng-02.txt]}
            elif lang not in filepaths_dictionary[edition].keys(): # if edition is not in lang.keys 
                filepaths_dictionary[edition][lang] = [txt] # create  {2020-01-ed1 : [eng-01.txt, eng-02.txt]}
            else: 
                filepaths_dictionary[edition][lang].append(txt) # add to edition list 2020-01-ed1 : [eng-01.txt] -> 2020-01-ed1 : [eng-01.txt, eng-02.txt]
                filepaths_dictionary[edition][lang].sort()

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

# {
#     "edition" : "",
#     "story_no" : "",
#     "langs" : {
#         "eng" : {
#             "title" : "",
#             "author" : "",
#             "text" : ""
#         },

#     }
# }


if __name__ == "__main__":
    file_paths = build_filepaths_dictonary()
    out_list = []
    for edition_key in file_paths.keys():
        edition = file_paths[edition_key]
        
        stories = {}
        story_nos = None
        for lang_key in edition.keys():
            stories[lang_key] = {}
            lang_txt_paths = edition[lang_key]
            story_nos = len(lang_txt_paths)

            for story_no, path in enumerate(lang_txt_paths):
                text = extract_text(Path(PROCESSED_PATH / edition_key / path))
                stories[lang_key][story_no] = text

        half_list = []
        for story_no in stories[lang_key].keys():
            out = {}
            out["languages"] = {}
            out["edition"] = edition_key
            out["story_no"] = story_no
            for lang in stories.keys():
                out["languages"][lang] = stories[lang_key][story_no]
            half_list.append(out)
        out_list.extend(half_list)
    write_to_json(out_list)
                
        