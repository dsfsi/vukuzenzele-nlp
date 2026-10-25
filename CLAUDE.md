# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About

The Vuk'uzenzele South African Multilingual Corpus: parallel and monolingual text from the government magazine *Vuk'uzenzele* in the 11 official South African languages. The repo covers PDF extraction, LASER-based sentence alignment, and conversion and upload of the datasets to HuggingFace (`dsfsi/vukuzenzele-monolingual`, `dsfsi/vukuzenzele-sentence-aligned`). It follows the Cookiecutter Data Science layout. `src/features`, `src/models`, `src/visualization` and `src/data/make_dataset.py` are unused template stubs.

## Commands

```bash
make requirements            # pip install -r requirements.txt (runs test_environment.py first)
make lint                    # flake8 src (tox.ini: max-line-length 79, max-complexity 10)
make clean                   # remove *.pyc / __pycache__

# 1. Extract one story from an edition's PDFs into data/interim/{edition}/
python src/data/vukuzenzele-extract.py -f 2020-01-ed1 --eng 3-7 --rest 4-8 --sn 01
#   --eng / --rest: page ranges for the English PDF and the other 10 language PDFs; --sn: zero-padded story number

# 2. Sentence alignment (only editions newer than last_edition_read.txt)
python3 src/sentence_alignment/main.py

# 3. Conversions / upload
python src/scripts/processed_to_json.py     # -> data/editions_json/
python src/scripts/processed_to_jsonl.py    # -> data/monolingual_jsonl/{lang}.jsonl (appends!)
HFTOKEN=... python src/scripts/push_to_huggingface.py
```

There is no test suite; `test_environment.py` only checks the Python version.

## Architecture

### Data flow

`data/raw/` (PDFs) → `vukuzenzele-extract.py` → `data/interim/` → **manual cleanup** → `data/processed/{edition}/` → alignment pipeline → `data/opt_aligned_out/aligned-{src}-{tgt}.jsonl`

- Processed files are named `{edition}-vukuzenzele-{lang}-{story}.txt`, e.g. `2018-01-ed1-vukuzenzele-eng-07.txt`. Edition format is `YYYY-MM-edN`.
- The processed file layout is positional: line 1 is the title, line 2 is blank, line 3 is the author, line 4 is blank, and the body follows. `processed_to_json(l).py` parses it by line index (`processed_to_jsonl.py` starts the body at index 5, so it skips the first body line).
- The language is detected everywhere by regex on the filename (`afr|eng|nso|nbl|sot|ssw|tsn|tso|ven|xho|zul`).

### Sentence alignment (`src/sentence_alignment/`)

Modules use flat imports (`import file_handler`), so run them as scripts from that directory's context (e.g. `python3 src/sentence_alignment/main.py`), not as a package.

`main.py` runs these stages:
1. **Edition selection.** `file_handler` reads `last_edition_read.txt` (it defaults to `2018-01-ed1`), converts edition names to dates (`edN` becomes the day), and keeps only the newer editions in `data/processed/`. `build_filepaths_dictonary()` (spelled that way in the code) is also limited to these new editions, giving `{lang: {edition: [files]}}`. When the run finishes, the file is set to the last edition processed. Delete or edit this file to reprocess editions.
2. **LASER setup** (`laser_config.py`). Runs the install scripts in the vendored `LASER/` (skipped if `LASER/models` and `LASER/tools-external` exist), downloads the NLLB LASER encoders for the languages mapped in `main.lang_mappings`, and downloads NLTK `punkt`. An empty mapping means the default LASER2 encoder is used.
3. **Tokenisation** (`sentence_tokenisation.py`). Lowercases the text, strips hyphens and bullets, normalises quotes and the Afrikaans `ŉ`, fixes missing spaces after full stops (keeping `.co.za` intact), then runs NLTK `sent_tokenize`. Output goes to `data/tokenised/`.
4. **Embedding** (`sentence_embedding.py`). Shells out to `LASER/tasks/embed/embed.sh` and writes raw float32 1024-dim vectors to `data/embed/`.
5. **Alignment** (`sentence_alignment.py`), run for every combination of the 11 languages (`itertools.combinations`). Edition `2018-02-ed1` is hard-skipped. Stories are paired **by sorted index** of the file lists, not by story number, so a story missing in one language misaligns every story after it. Within a story the alignment is greedy and monotonic, using windows of 5:
   - A window is rejected if its first pair scores below 0.7.
   - A window ends at the first pair scoring below 0.6.
   - On failure, `update_indices` searches a 3×3 neighbourhood for a pair scoring above 0.7.

   Results are **appended** to the JSONL files as `{src: ..., tgt: ..., "score": ...}`.

The 0.65 cosine cutoff reported in the README is applied afterwards as a filter (`count_aligned_pairs`); it is not part of alignment. The `simple_langs_alignment` and CSV writers in `file_handler.py` belong to older output formats (`data/simple_align_output/`, `data/sentence_align_output/`), and their calls in `main.py` are commented out.

### Language codes

The code uses 11 codes: `afr eng nbl nso sot ssw tsn tso ven xho zul`. `sot` is Sesotho (`sot_Latn`) and `nso` is Sepedi/Northern Sotho (`nso_Latn`). Older material (`data/.temp/`, `data/raw/2019-08-ed2/Sent/`, early commits) uses `sep` for Sepedi.

### CI

`.github/workflows/perform_sentence_alignment.yml` runs `main.py` on Python 3.8 on the 1st of every second month (and on `workflow_dispatch`), then auto-commits any changed outputs, including `last_edition_read.txt`.
