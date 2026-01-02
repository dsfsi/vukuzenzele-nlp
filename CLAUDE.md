# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About

The Vuk'uzenzele South African Multilingual Corpus is a dataset containing parallel text data from the South African government magazine Vuk'uzenzele in 11 South African languages. The repository handles PDF extraction, sentence alignment using LASER encoders, and dataset preparation for HuggingFace.

## Development Commands

### Environment Setup
```bash
# Install dependencies
python3 -m pip install -U pip setuptools wheel
python3 -m pip install -r requirements.txt

# Or use Make
make requirements

# Test environment
python3 test_environment.py
```

### Data Processing Pipeline

**Extract text from PDFs:**
```bash
python src/data/vukuzenzele-extract.py -f "folder-name" --eng "1-5" --rest "2-6" --sn "01"
# Example: python src/data/vukuzenzele-extract.py -f 2020-01-ed1 --eng 3-7 --rest 4-8 --sn 01
```
- `--eng`: Page range for English version
- `--rest`: Page range for other 10 languages
- `--sn`: Story number (zero-padded)
- Extracted files go to `data/interim/{edition}/` and need manual refinement before moving to `data/processed/`

**Perform sentence alignment:**
```bash
python3 src/sentence_alignment/main.py
```
This runs the full sentence alignment pipeline using LASER embeddings.

### Data Format Conversion

**Convert processed data to JSON:**
```bash
python src/scripts/processed_to_json.py
```

**Convert to JSONL format:**
```bash
python src/scripts/processed_to_jsonl.py
```

**Push to HuggingFace:**
```bash
# Requires HFTOKEN environment variable
export HFTOKEN=your_token_here
python src/scripts/push_to_huggingface.py
```

### Code Quality
```bash
make lint    # Run flake8 on src/
make clean   # Remove compiled Python files
```

## Architecture Overview

### Data Flow Pipeline

1. **Raw PDFs** (`data/raw/`) → Magazine PDFs organized by edition (e.g., `2020-01-ed1/`)

2. **Extraction** (`src/data/vukuzenzele-extract.py`) → Extracts text from PDFs to `data/interim/`
   - Handles column-to-row conversion, page separators, hyphenation fixes
   - Requires manual refinement before processing

3. **Processed Data** (`data/processed/`) → Manually cleaned text files, organized by edition

4. **Sentence Alignment Pipeline** (`src/sentence_alignment/main.py`):
   - **Tokenisation** → Cleans and tokenizes sentences (`sentence_tokenisation.py`)
   - **LASER Encoding** → Embeds sentences using LASER models (`sentence_embedding.py`)
   - **Alignment** → Aligns sentences across language pairs using cosine similarity (`sentence_alignment.py`)
   - **Output** → CSV files in `data/opt_aligned_out/` with aligned sentence pairs

5. **Format Conversion** (`src/scripts/`) → Converts to JSON/JSONL for HuggingFace upload

### Key Modules

**`src/sentence_alignment/`** - Core sentence alignment logic using LASER
- `main.py`: Orchestrates the alignment pipeline for new editions
- `file_handler.py`: File I/O operations, builds filepath dictionaries, tracks processed editions
- `laser_config.py`: Downloads and configures LASER models and tokenizers
- `sentence_embedding.py`: Encodes sentences using LASER language encoders
- `sentence_alignment.py`: Performs alignment using cosine similarity on embeddings
- `sentence_tokenisation.py`: Tokenizes and cleans text
- `last_edition_read.txt`: Tracks last processed edition to avoid reprocessing
- `LASER/`: Facebook Research's LASER module for multilingual sentence embeddings

**`src/scripts/`** - Data conversion utilities
- `processed_to_json.py`: Converts processed data to JSON format
- `processed_to_jsonl.py`: Converts to JSONL format
- `push_to_huggingface.py`: Uploads datasets to HuggingFace Hub (requires HFTOKEN)

### Language Codes

The corpus includes 11 South African languages with specific LASER model mappings:

| Language   | Code | LASER Model    |
|------------|------|----------------|
| English    | eng  | (default)      |
| Afrikaans  | afr  | (default)      |
| isiNdebele | nbl  | (default)      |
| isiXhosa   | xho  | xho_Latn       |
| isiZulu    | zul  | zul_Latn       |
| Sesotho    | nso  | nso_Latn       |
| Sepedi     | sep  | (unused in SA) |
| Setswana   | tsn  | tsn_Latn       |
| Siswati    | ssw  | ssw_Latn       |
| Tshivenda  | ven  | (default)      |
| Xitstonga  | tso  | tso_Latn       |

Note: `sot` (Sesotho) vs `nso` (Northern Sotho/Sepedi) - code uses both; check context.

### Data Directory Structure

```
data/
├── raw/                      # Raw magazine PDFs organized by edition
├── interim/                  # Extracted text needing manual refinement
├── processed/                # Manually cleaned text files by edition
├── opt_aligned_out/          # LASER-aligned sentence pairs (CSV)
├── simple_align_output/      # Simple 1:1 alignment output (CSV)
├── sentence_align_output/    # Alternative alignment output
├── editions_json/            # JSON format output
├── monolingual_jsonl/        # JSONL format for monolingual data
└── huggingface/              # Prepared datasets for HuggingFace
```

### Alignment Process Details

The sentence alignment uses LASER (Language-Agnostic SEntence Representations):
1. Text is tokenized and cleaned
2. Sentences are embedded into a shared vector space using language-specific LASER models
3. Cosine similarity between embeddings is calculated
4. Sentence pairs with similarity >= 0.65 are considered aligned
5. Results are saved as CSV with source/target language pairs

The pipeline processes all possible language pair combinations and tracks progress to avoid reprocessing editions.

## GitHub Actions

The repository has a scheduled workflow (`.github/workflows/perform_sentence_alignment.yml`) that:
- Runs bi-monthly on the 1st day of every 2nd month at 12:00 UTC
- Can be triggered manually via workflow_dispatch
- Executes `src/sentence_alignment/main.py` to process new editions
- Auto-commits results if any changes are detected

## Important Notes

- PDF extraction requires manual verification and refinement - automated extraction cannot perfectly separate titles, authors, and content
- The alignment pipeline uses `last_edition_read.txt` to track progress and skip already-processed editions
- When working with HuggingFace uploads, set the `HFTOKEN` environment variable
- The codebase follows a Cookiecutter Data Science project structure
- Edition naming format: `YYYY-MM-edN` (e.g., `2020-01-ed1`)
