import os, pandas 
from pathlib import Path
ROOT_PATH = Path(os.path.abspath(__file__)).parent.parent.parent
DATA_PATH = Path(ROOT_PATH / 'data' / 'opt_aligned_out')

if __name__ == "__main__":
    aligned = os.listdir(DATA_PATH)
    aligned.sort()
    print('pair\t\tlength\taligned above 0.65')
    for a in aligned:
        df = pandas.read_json(f"{DATA_PATH}/{a}", lines=True)
        count = (df['score'] > 0.65).sum()
        print("{}\t\t{}\t{}".format(a[8:15], len(df), count))