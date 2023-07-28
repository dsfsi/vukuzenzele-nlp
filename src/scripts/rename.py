import os, re
from pathlib import Path

# Define paths for different directories
REPO_PATH = Path(os.path.abspath(__file__)).parent.parent.parent
DATA_PATH = Path(REPO_PATH / 'data')

RAW_PATH = Path(DATA_PATH / 'raw')
INTERIM_PATH = Path(DATA_PATH / 'interim')
PROCESSED_PATH = Path(DATA_PATH / 'processed')

SENTENCE_ALIGNED_PATH = Path(DATA_PATH / 'sentence_align_output')
SIMPLE_ALIGNED_PATH = Path(DATA_PATH / 'simple_align_output')

# List of directories where data needs to be renamed
DATA_DIRS  = [RAW_PATH, INTERIM_PATH, PROCESSED_PATH,]
# List of directories where output data needs to be renamed
OUT_DIRS = [SENTENCE_ALIGNED_PATH, SIMPLE_ALIGNED_PATH]

# Function to rename language codes in the data directories
def rename_data_dirs(src_lang_code, tgt_lang_code):
    for data_dir in DATA_DIRS:
        print(data_dir)
        # List all editions (subdirectories) within the data directory
        editions = os.listdir(data_dir)

        # Remove unwanted files/folders from the list (if present)
        if '.DS_Store' in editions: editions.remove('.DS_Store')
        if '.gitkeep' in editions: editions.remove('.gitkeep')
        if 'README.md' in editions: editions.remove('README.md')

        # Process each edition in the data directory
        for ed in editions:
            ed_path = Path(data_dir / ed)

            if os.path.exists(ed_path):
                # List all files within the edition directory
                files = os.listdir(ed_path)

                # Process each file in the edition directory
                for f in files:
                    source = "{}/{}".format(ed_path, f)

                    # Check if the source file name contains the source language code
                    if re.search(src_lang_code, f):
                        # Replace the source language code with the target language code
                        new = re.sub(src_lang_code, tgt_lang_code, f)
                        dest = "{}/{}".format(ed_path, new)
                        # Rename the file with the updated language code
                        os.rename(source, dest)

# Function to rename language codes in the output directories
def rename_out_dirs(src_lang_code, tgt_lang_code):
    for out_dir in OUT_DIRS:
        # List all output files within the output directory
        out_paths = os.listdir(out_dir)

        # Process each output file in the output directory
        for out in out_paths:
            source = "{}/{}".format(out_dir, out)

            # Check if the source file name contains the source language code
            if re.search(src_lang_code, out):
                # Replace the source language code with the target language code
                new = re.sub(src_lang_code, tgt_lang_code, out)
                dest = "{}/{}".format(out_dir, new)
                # Rename the output file with the updated language code
                os.rename(source, dest)

# Main function
if __name__ == "__main__":
    # Rename data directories from 'nso' to 'sot'
    rename_data_dirs('nso', 'sot')
    # Rename data directories from 'sep' to 'nso'
    rename_data_dirs('sep', 'nso')
    # Rename output directories from 'nso' to 'sot'
    rename_out_dirs('nso', 'sot')
    # Rename output directories from 'sep' to 'nso'
    rename_out_dirs('sep', 'nso')
