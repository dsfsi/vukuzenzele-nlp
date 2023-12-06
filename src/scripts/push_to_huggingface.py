from pathlib import Path
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from datasets import Dataset, DatasetDict

REPO_PATH = Path(os.path.abspath(__file__)).parent.parent.parent
DATA_PATH = Path(REPO_PATH / "data")
ALIGNED_PATH = Path(DATA_PATH / "opt_aligned_out")
MONO_PATH = Path(DATA_PATH / "monolingual_jsonl")
OUT_PATH = Path(DATA_PATH / "vukuzenzele-sentence-aligned")


if __name__ == "__main__":
    aligned_paths = os.listdir(MONO_PATH)
    aligned_paths.sort()
    token = os.environ.get('HFTOKEN')
    big_dict = {}
    for i, path in enumerate(aligned_paths):
    #     if i < 41: continue
        lang = path[:3]
        print(lang)

        file_path = os.path.join(MONO_PATH, path)

        df = pd.read_json(file_path, lines=True)
        train_df, test_df = train_test_split(df, test_size=0.3, random_state=42)
        test_df, eval_df = train_test_split(test_df, test_size=0.5, random_state=42)

    #     # Create a DatasetDict
        dataset_dict =  DatasetDict({
                "train": Dataset.from_pandas(train_df),
                "test": Dataset.from_pandas(test_df),
                "eval": Dataset.from_pandas(eval_df),
            })
        
        dataset_dict.push_to_hub('dsfsi/vukuzenzele-monolingual', lang)


    # dataset = DatasetDict(big_dict)
    # dataset.push_to_hub('dsfsi/vukuzenzele-sentence-aligned')