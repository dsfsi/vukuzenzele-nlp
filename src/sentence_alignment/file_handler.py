import os, re, json, pandas
from pathlib import Path
from datetime import date

root_path = Path(os.path.abspath(__file__)).parent.parent.parent # vukuzenzele/

raw_data_path = Path(root_path / 'data' / 'processed') #data/processed - raw in terms of sentence alignment
token_data_path = Path(root_path  / 'data' / 'tokenised') #data/tokenised - the tokenised form
output_data_path = Path(root_path / 'data' / 'sentence_align_output') #data/sentence_align_output - SA using encoders
simp_out_data_path = Path(root_path / 'data' / 'simple_align_output')  #data/simple_align_output - plain SA, eg `hello` -> `hallo`
out_path = Path(root_path / "data" / "opt_aligned_out")

languages = ['afr', 'eng', 'nbl', 'nso', 'sot', 'ssw', 'tsn', 'tso', 'ven', 'xho', 'zul'] # List of SA languages


def extract_latest_edition():
    """
    ### Reads the value stored in `last_edition_read.txt` which stores the last edition which underwent SA.
    """

    file_path =  Path(
            Path(os.path.abspath(__file__)).parent #src/sentence_alignment
            / 'last_edition_read.txt' 
        )

    if not os.path.exists(file_path):
        open(file_path , 'w')

    edition = open(file_path,'r').read() #read as str

    if not re.match('^\d{4}-\d{2}-[a-z]{2}\d$', edition): 
        edition = '2020-01-ed1'
    return edition

def write_latest_edition(edition):
    """
    Writes an edition to last_edition_read.txt
    """
    open(
        Path(
            Path(os.path.abspath(__file__)).parent #src/sentence_alignment
            / 'last_edition_read.txt'
        ),'w').write(edition)

def build_date(edition):
    """
    Builds a date object using REGEX off an edition name, eg. 2020-01-ed2 = 2020/01/02
    """
    edition_date = re.search('^\d{4}-\d{2}', edition).group()
    edition_no = re.search('\d$',edition).group()

    year = re.search('^\d{4}', edition_date).group()
    month = re.search('\d{2}$', edition_date).group()
    day = edition_no

    return date(int(year), int(month), int(day))

def fetch_data_edition_filepaths(last_date): # -> list[str]
    """
    ### Compiles a list of file directories present in the /data/processed folder after the date present in /last_edition_read.txt
    #### Example filepath: `2020-01-ed1`
    """
    all_paths = os.listdir(raw_data_path) # list the directories in /data/processed
    all_paths.remove('.gitkeep') # remove the .gitkeep
    try: all_paths.remove('.DS_Store') 
    except: pass # remove the .DS
    all_paths.sort() # sort them

    edition_paths = [] # empty list to append to
    for path in all_paths:
        if build_date(path) > build_date(last_date): # if curr path later than last_date
            edition_paths.append(path) # add to edition paths
    edition_paths.sort() # the strings are sorted the same way date's would be... if only I knew sooner
    return edition_paths

def fetch_data_txt_filepaths(edition): # -> list[str]
    """
    ### Compiles a list of files present in the /data/processed/edition folder
    #### Example filepath: `2020-02-ed1-vukuzenzele-afr-01.txt`
    #### Params 
        -   `edition` is the different editions of the magazine stored in data/processed
    """
    txt_paths = os.listdir('{}/{}'.format(raw_data_path, edition)) # list the directories in /data/processed/edition
    return txt_paths

def build_filepaths_dictonary():
    """
    ### Creates a dict for every lang. 
    #### Example
    ```
    {
        'eng' : {
            '2020-09-ed1' : [
                '2020-09-ed1-vukuzenzele-eng-001.txt',  
                '2020-09-ed1-vukuzenzele-eng-002.txt',  
                '2020-09-ed1-vukuzenzele-eng-003.txt'  
            ]
        }
        'afr' : {
            '2020-09-ed1' : [
                '2020-09-ed1-vukuzenzele-afr-001.txt',  
                '2020-09-ed1-vukuzenzele-afr-002.txt',  
                '2020-09-ed1-vukuzenzele-afr-003.txt'  
            ]
        }
    }
    ```
    """
    filepaths_dictionary = {} # empty dict to append to
    edition_paths = fetch_data_edition_filepaths(extract_latest_edition()) # build edition keys
    for edition in edition_paths: # for each edition
        txt_paths = fetch_data_txt_filepaths(edition) # list of txt paths inside an edition dir
        for txt in txt_paths: #for each txt file
            lang = re.search('afr|eng|nso|nbl|sot|ssw|tsn|tso|ven|xho|zul', txt).group() # what lang is it 
            if lang not in filepaths_dictionary.keys(): # if lang is not present in dict
                filepaths_dictionary[lang] = {edition : [txt]} # create end : { 2020-01-ed1 : [eng-01.txt, eng-02.txt]}
            elif edition not in filepaths_dictionary[lang].keys(): # if edition is not in lang.keys 
                filepaths_dictionary[lang][edition] = [txt] # create  {2020-01-ed1 : [eng-01.txt, eng-02.txt]}
            else: 
                filepaths_dictionary[lang][edition].append(txt) # add to edition list 2020-01-ed1 : [eng-01.txt] -> 2020-01-ed1 : [eng-01.txt, eng-02.txt]

    return filepaths_dictionary 

def read_file_as_string(edition_path, txt_path): # -> str
    """
    ### Reads file as a single string. 

    Generally used to read file as string to be passed to tokeniser
    """
    file_path = Path(raw_data_path / edition_path / txt_path)
    return open(file_path, 'r').read() 

def read_file_as_array(edition_path, txt_path): # -> str
    """
    ### Reads file as an array.

    Generally used to read tokenised data for further processing
    """
    file_path = Path(token_data_path / edition_path / txt_path)
    return open(file_path, 'r').readlines() 


def write_tokens_to_txt(edition_path, txt_path, tokens): # -> None
    """
    ### Writes a token array to a .txt in the data/tokenised folder
    #### Params:
        -   edition_path: path_name representing the edition to create a new dir for the tokens
        -   txt_path: path_name to the sentence tokens to create a new txt file
        -   tokens: list of sentence tokens to be written to file
    """
    if not os.path.exists(Path(token_data_path / edition_path)): #if data/tokenised/edition does not exist
        os.makedirs((Path(token_data_path / edition_path))) # create it

    new = open((Path(token_data_path / edition_path / txt_path)),'w') # open a txt file in write mode
    for token in tokens: #for each tokem
        new.write(token) # write to new file
        if not tokens[len(tokens)-1]==token: # the tokens seem to be missing newlines so if token is not the last token,
            new.write('\n')  # write a newline

def append_to_final_csv(src_lang, src_sentences, tgt_lang, tgt_sentences , sim_scores):
    """
    ### Appends to the ML aligned lang pairs .csv - creates it if it doesn't exist
    #### Params
        -   src_lang: source lang (str)
        -   src_sentences: source sentence tokens (list)
        -   src_vector: source sentence vectors (list)
        -   tgt_lang: target lang (str)
        -   tgt_sentences: target sentence tokens (list)
        -   tgt_vector: target sentence vectors (list)
        -   sim_scores: confidence scores between the pairing (list)
    """
    data = {
        'src_text' : src_sentences,
        'tgt_text' : tgt_sentences,
        'cosine_score' : sim_scores
    } # build a dictonary of the info

    df = pandas.DataFrame(data) #turn into a pandas DF

    csv_path = Path('aligned_{}_{}.csv'.format(src_lang, tgt_lang)) # Path of lang aligned csv
    if not os.path.exists(output_data_path): # if data/sentence_alignment doesnt exist
        os.makedirs(output_data_path) # create it 

    if os.path.exists(Path(output_data_path / csv_path)): # if .csv does exist
        df.to_csv(Path(output_data_path / csv_path), mode='a',header=False, index=False) # append with no headers
    else: 
        df.to_csv(Path(output_data_path / csv_path), mode='w',header=True, index=False) # create with headers


def append_to_simple_csv(src_lang, src_sentences, tgt_lang, tgt_sentences):

    data = {
        src_lang : src_sentences,
        tgt_lang : tgt_sentences,
    }
    df = pandas.DataFrame(data)

    csv_path = Path('aligned_{}_{}.csv'.format(src_lang, tgt_lang))
    if not os.path.exists(simp_out_data_path):
        os.makedirs(simp_out_data_path)

    if os.path.exists(Path(output_data_path / csv_path)):
        df.to_csv(Path(simp_out_data_path / csv_path), mode='a',header=False, index=False)
    else: 
        df.to_csv(Path(simp_out_data_path / csv_path), mode='w',header=True, index=False)

def write_to_jsonl(src,tgt,edition,data):
    file_name = "aligned-{}-{}.jsonl".format(src, tgt)
    file_path = out_path  / file_name

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    if file_name in os.listdir(out_path):
        f = open(file_path, 'a')
        for d in data:
            f.write(json.dumps(d) + '\n')
    else:
        f = open(file_path, 'w')
        for d in data:
            f.write(json.dumps(d) + '\n')

    # print("Aligned {}-{} from Cab Statement on {}".format(src,tgt, date))

def count_aligned_pairs():
    with open("filtered_data.txt", 'w') as filtered_file:
        csv_files = os.listdir(output_data_path)
        filtered_file.write("|----------|----------|-------------------|\n")
        filtered_file.write("| src_lang | trg_lang | num_aligned_pairs |\n")
        filtered_file.write("|----------|----------|-------------------|\n")

        for csv_file in csv_files:
            df = pandas.read_csv(output_data_path / Path(csv_file))
            df = df[df["cosine_score"] >= 0.65]
            strip_file_name = re.split("[_.]", csv_file)

            filtered_file.write("|" + " " + strip_file_name[1] +" " * 5 + " " + "|" + " " + strip_file_name[2] + " " * 5 + " " + "|" + " " + str(len(df)) + " " * (17 - len(str(len(df)))) + " " + "|\n")
    
        filtered_file.write("|----------|----------|-------------------|\n")