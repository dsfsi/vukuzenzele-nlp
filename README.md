# The Vuk'uzenzele South African Multilingual Corpus

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7598539.svg)](https://doi.org/10.5281/zenodo.7598539)
[![arXiv](https://img.shields.io/badge/arXiv-2303.03750-b31b1b.svg)](https://arxiv.org/abs/2303.03750)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE.data.md)
[![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97-Datasets-yellow)](https://huggingface.co/datasets/dsfsi/vukuzenzele-monolingual)

> A multilingual parallel corpus from South African government publications in 11 official languages

## Overview

The Vuk'uzenzele South African Multilingual Corpus contains text data extracted from the South African government magazine [Vuk'uzenzele](https://www.vukuzenzele.gov.za/), published by the [Government Communication and Information System (GCIS)](https://www.gcis.gov.za/). This corpus provides valuable parallel text data across 11 South African languages, making it an important resource for multilingual NLP research in African languages.

### Coverage

- **Raw data**: 192 editions from **November 2012 to December 2022**
- **Processed & aligned data**: 84 editions from **January 2018 to December 2022**
- **Languages**: 11 South African official languages
- **Total aligned pairs**: 165,757 sentence pairs (159,987 with cosine score >= 0.65) across 55 language pair combinations

### Access the Datasets

📦 **HuggingFace Datasets**:
- [Monolingual dataset](https://huggingface.co/datasets/dsfsi/vukuzenzele-monolingual) - Individual language data with train/test/eval splits
- [Sentence-aligned dataset](https://huggingface.co/datasets/dsfsi/vukuzenzele-sentence-aligned) - Parallel sentence pairs across language combinations

📚 **Zenodo Archive**: [https://doi.org/10.5281/zenodo.7598539](https://doi.org/10.5281/zenodo.7598539)

📄 **Research Paper**: [ACL Anthology](https://aclanthology.org/2023.rail-1.3) | [arXiv](https://arxiv.org/abs/2303.03750)

💬 **Give Feedback**: [DSFSI Resource Feedback Form](https://docs.google.com/forms/d/e/1FAIpQLSf7S36dyAUPx2egmXbFpnTBuzoRulhL5Elu-N1eoMhaO7v10w/formResponse)

## Languages

The corpus includes all 11 South African official languages:

|  Language  | Code |  Language  | Code |
|------------|-------|------------|-------|
| English    | eng   | Sepedi     | nso   |
| Afrikaans  | afr   | Setswana   | tsn   |
| isiNdebele | nbl   | Siswati    | ssw   |
| isiXhosa   | xho   | Tshivenda  | ven   |
| isiZulu    | zul   | Xitstonga  | tso   |
| Sesotho    | sot   |            |       |

### Number of Aligned Pairs with Cosine Similarity Score >= 0.65

Counted from `data/opt_aligned_out/` (the files published as the HuggingFace sentence-aligned dataset).

|src_lang|trg_lang|num_aligned_pairs|
|--------|--------|-----------------|
|xho|zul|4,628|
|ssw|zul|4,610|
|ssw|xho|4,483|
|ssw|tso|4,402|
|ssw|tsn|4,368|
|tso|zul|4,345|
|sot|xho|4,328|
|sot|zul|4,296|
|afr|xho|4,295|
|tso|xho|4,281|
|nso|sot|4,273|
|sot|ssw|4,273|
|afr|zul|4,268|
|sot|tso|4,253|
|sot|tsn|4,249|
|tsn|tso|4,231|
|tsn|zul|4,225|
|afr|ssw|4,213|
|nso|zul|4,177|
|nso|tso|4,146|
|nso|ssw|4,133|
|tsn|xho|4,133|
|nso|tsn|4,100|
|afr|sot|4,099|
|afr|tso|4,091|
|nso|xho|4,087|
|afr|nso|4,054|
|afr|tsn|3,884|
|eng|sot|3,744|
|afr|eng|3,713|
|eng|ssw|3,711|
|eng|zul|3,702|
|eng|tso|3,692|
|eng|xho|3,686|
|eng|nso|3,674|
|nbl|ven|3,562|
|eng|tsn|3,521|
|afr|ven|959|
|afr|nbl|784|
|sot|ven|541|
|ssw|ven|476|
|ven|xho|464|
|nbl|xho|447|
|tso|ven|447|
|tsn|ven|436|
|nbl|ssw|419|
|nbl|sot|408|
|nso|ven|405|
|ven|zul|392|
|nbl|tsn|336|
|nbl|zul|336|
|nbl|tso|330|
|eng|ven|329|
|nbl|nso|306|
|eng|nbl|242|

## Getting Started

### Quick Start with HuggingFace

```python
from datasets import load_dataset

# Load monolingual data for a specific language
dataset = load_dataset("dsfsi/vukuzenzele-monolingual", "zul")  # isiZulu
print(dataset['train'][0])

# Load sentence-aligned parallel data
aligned_dataset = load_dataset("dsfsi/vukuzenzele-sentence-aligned", "eng-zul")
```

### Repository Structure

The repository contains data in multiple stages of processing:

```
./data
├── raw/                     # Raw PDFs of Vuk'uzenzele magazine (2012-2022, 192 editions)
├── interim/                 # Extracted text requiring manual refinement
├── processed/               # Manually cleaned text files (2018-2022, 84 editions)
├── opt_aligned_out/         # LASER-aligned sentence pairs (JSONL, one file per language pair)
├── sentence_align_output/   # Older LASER alignment output (CSV, superseded by opt_aligned_out)
├── simple_align_output/     # Simple 1:1 sentence alignment (CSV)
├── editions_json/           # JSON format outputs
├── monolingual_jsonl/       # JSONL format for HuggingFace
└── huggingface/             # Prepared datasets for HuggingFace Hub
```

Each edition follows the naming format: `YYYY-MM-edN` (e.g., `2020-01-ed1`).

## Contributing

**We welcome contributions!** There are several ways you can help expand this corpus:

### Add More Years 🎯

The Vuk'uzenzele magazine has been published since October 2005, but our corpus currently only covers **November 2012 to December 2022**. We need help expanding coverage to:
- **Earlier years**: 2005-2012 editions
- **Recent years**: 2023 onwards

### How to Contribute

1. **Download PDFs**: Get Vuk'uzenzele PDFs from the [official archive](https://www.vukuzenzele.gov.za/)
2. **Extract text**: Follow the extraction workflow in [CLAUDE.md](CLAUDE.md) or [src/data/ReadME.md](src/data/ReadME.md)
3. **Refine data**: Manually clean extracted text to ensure quality
4. **Submit PR**: Create a pull request with your additions

### Other Ways to Help

- **Improve alignment**: Enhance sentence alignment algorithms
- **Add metadata**: Extract publication dates, authors, topics
- **Quality control**: Review and correct existing alignments
- **Documentation**: Improve guides and examples
- **Applications**: Build NLP models and share results

See our [GitHub Issues](https://github.com/dsfsi/vukuzenzele-nlp/issues) for specific tasks or create a new issue to discuss your ideas!

### Development Setup

```bash
# Clone the repository
git clone https://github.com/dsfsi/vukuzenzele-nlp.git
cd vukuzenzele-nlp

# Install dependencies
pip install -r requirements.txt

# See CLAUDE.md for detailed development commands
```

## Applications & Uses

This corpus has been used for:
- **Machine Translation**: Training translation models for South African language pairs
- **Language Models**: Pretraining multilingual models like [PuoBERTa](https://huggingface.co/dsfsi/PuoBERTa)
- **Speech Recognition**: Creating the [Vukuzenzele isiXhosa Speech Dataset](https://huggingface.co/datasets/lelapa/Vukuzenzele_isiXhosa_Speech_Dataset_ViXSD)
- **Cross-lingual Transfer**: Evaluating multilingual NLP systems
- **Low-resource Language Research**: Advancing NLP for under-resourced African languages

## Citation

If you use this corpus in your research, please cite:

### Paper

```bibtex
@inproceedings{lastrucci-etal-2023-preparing,
    title = "Preparing the Vuk{'}uzenzele and {ZA}-gov-multilingual {S}outh {A}frican multilingual corpora",
    author = "Richard Lastrucci and Isheanesu Dzingirai and Jenalea Rajab and Andani Madodonga and Matimba Shingange and Daniel Njini and Vukosi Marivate",
    booktitle = "Proceedings of the Fourth workshop on Resources for African Indigenous Languages (RAIL 2023)",
    month = may,
    year = "2023",
    address = "Dubrovnik, Croatia",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.rail-1.3",
    pages = "18--25"
}
```

### Dataset

```bibtex
@dataset{marivate_vukosi_2023_7598540,
  author       = {Marivate, Vukosi and
                  Njini, Daniel and
                  Madodonga, Andani and
                  Lastrucci, Richard and
                  Dzingirai, Isheanesu and
                  Rajab, Jenalea},
  title        = {The Vuk'uzenzele South African Multilingual Corpus},
  month        = feb,
  year         = 2023,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.7598539},
  url          = {https://doi.org/10.5281/zenodo.7598539}
}
```

## Authors & Contributors

**Core Team**:
- [Vukosi Marivate](https://twitter.com/vukosi) - Project Lead
- Andani Madodonga
- Daniel Njini
- Richard Lastrucci
- Isheanesu Dzingirai
- Jenalea Rajab

Affiliated with the [Data Science for Societal Impact Research Group](https://dsfsi.github.io/)

## License

- **Data**: [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE.data.md)
- **Code**: [MIT License](LICENSE.md)

## Disclaimer

This dataset contains machine-readable data extracted from PDF documents from [https://www.vukuzenzele.gov.za/](https://www.vukuzenzele.gov.za/), provided by the Government Communication Information System (GCIS). While efforts were made to ensure accuracy and completeness, there may be errors or discrepancies between the original publications and this dataset.

No warranties, guarantees, or representations are given regarding the information in this dataset. Neither the Data Science for Societal Impact Research Group nor the Government Communication Information System (GCIS) bear responsibility for any errors or discrepancies. Users should verify all information before making decisions based on this data.

---

**Maintained by**: [Data Science for Societal Impact Research Group (DSFSI)](https://dsfsi.github.io/)

**Contact**: Create an issue or use our [feedback form](https://docs.google.com/forms/d/e/1FAIpQLSf7S36dyAUPx2egmXbFpnTBuzoRulhL5Elu-N1eoMhaO7v10w/formResponse)
