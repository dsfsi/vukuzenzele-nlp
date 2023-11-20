from pathlib import Path
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from datasets import Dataset, DatasetDict

REPO_PATH = Path(os.path.abspath(__file__)).parent.parent.parent
DATA_PATH = Path(REPO_PATH / "data")
ALIGNED_PATH = Path(DATA_PATH / "opt_aligned_out")
OUT_PATH = Path(DATA_PATH / "vukuzenzele-sentence-aligned")


if __name__ == "__main__":
    aligned_paths = os.listdir(ALIGNED_PATH)
    aligned_paths.sort()
    token = os.environ.get('HFTOKEN')
    print(len(aligned_paths))
    for i, path in enumerate(aligned_paths):
        if i <= 48: continue
        src_tgt_list = path.split("-")
        src = src_tgt_list[1]  # First element
        tgt = src_tgt_list[2].split(".")[0]  # Second element

        file_path = os.path.join(ALIGNED_PATH, path)

        df = pd.read_json(file_path, lines=True)
        train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

        src_tgt_list = path.split("-")
        src = src_tgt_list[1]  # First element
        tgt = src_tgt_list[2].split(".")[0]  # Second element

        print(f'\n{i} :{src}-{tgt}\n')
        # Create a DatasetDict
        dataset_dict = DatasetDict(
            {
                "train": Dataset.from_pandas(train_df),
                "test": Dataset.from_pandas(test_df),
            }
        )
        # dataset_dict.push_to_hub('dsfsi/vukuzenzele-sentence-aligned', f'{src}-{tgt}')
        path = os.path.join(OUT_PATH / f'{src}-{tgt}' )
        os.makedirs(path)
        dataset_dict.save_to_disk(path)
        # train_df.to_parquet(os.path.join(path, 'train.parquet'))
        # test_df.to_parquet(os.path.join(path, 'test.parquet'))