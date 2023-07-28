import os, re
from pathlib import Path

REPO_PATH = Path(os.path.abspath(__file__)).parent.parent.parent
DATA_PATH = Path(REPO_PATH / 'data')

RAW_PATH = Path(DATA_PATH / 'raw')
INTERIM_PATH = Path(DATA_PATH / 'interim')
PROCESSED_PATH = Path(DATA_PATH / 'processed')

SENTENCE_ALIGNED_PATH = Path(DATA_PATH / 'sentence_align_output')
SIMPLE_ALIGNED_PATH = Path(DATA_PATH / 'simple_align_output')
 
DATA_DIRS  = [RAW_PATH, INTERIM_PATH, PROCESSED_PATH,]
OUT_DIRS = [SENTENCE_ALIGNED_PATH, SIMPLE_ALIGNED_PATH]

def rename_data_dirs():
    for data_dir in DATA_DIRS:
        print(data_dir)
        editions = os.listdir(data_dir)
        
        if '.DS_Store' in editions: editions.remove('.DS_Store')
        if '.gitkeep' in editions: editions.remove('.gitkeep')
        if 'README.md' in editions: editions.remove('README.md')

        for ed in editions:
            ed_path = Path(data_dir / ed )

            if os.path.exists(ed_path):
                files = os.listdir(ed_path)

                for f in files:
                    source = "{}/{}".format(ed_path,f)
                    
                    # if re.search('nso', f):
                    #     new = re.sub('nso', 'sot', f)
                    #     dest = "{}/{}".format(ed_path,new)
                    #     os.rename(source, dest)

                    if re.search('sep', f):
                        new = re.sub('sep', 'nso', f)
                        dest = "{}/{}".format(ed_path,new)
                        os.rename(source, dest)

def rename_out_dirs():
    for out_dir in OUT_DIRS:
        out_paths = os.listdir(out_dir)
        for out in out_paths:
            source = "{}/{}".format(out_dir,out)
            print(source)
            if re.search('nso', out):
                new = re.sub('nso', 'sot', out)
                dest = "{}/{}".format(out_dir,new)
                os.rename(source, dest)

            # if re.search('sep', out):
            #     new = re.sub('sep', 'nso', out)
            #     dest = "{}/{}".format(out_dir,new)
            #     os.rename(source, dest)

        
if __name__ == "__main__":
    rename_data_dirs()
    # rename_out_dirs()
           
    
            