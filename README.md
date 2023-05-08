# The Vuk'uzenzele South African Multilingual Corpus

Github: [https://github.com/dsfsi/vukuzenzele-nlp/](https://github.com/dsfsi/vukuzenzele-nlp/)

Zenodo: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7598539.svg)](https://doi.org/10.5281/zenodo.7598539)

Arxiv Preprint: [![arXiv](https://img.shields.io/badge/arXiv-2303.03750-b31b1b.svg)](https://arxiv.org/abs/2303.03750)

## About dataset
The dataset contains editions from the South African government magazine Vuk'uzenzele, created by the [Government Communication and Information System (GCIS)](https://www.gcis.gov.za/). Data was scraped from PDFs that have been placed in the [data/raw](data/raw/) folder.
The PDFS were obtatined from the [Vuk'uzenzele website](https://www.vukuzenzele.gov.za/).

The datasets contain government magazine editions in 11 languages, namely:

|  Language  | Code |  Language  | Code |
|------------|-------|------------|-------|
| English    | (eng) | Sepedi     | (sep) |
| Afrikaans  | (afr) | Setswana   | (tsn) |
| isiNdebele | (nbl) | Siswati    | (ssw) |
| isiXhosa   | (xho) | Tshivenda  | (ven) |
| isiZulu    | (zul) | Xitstonga  | (tso) |
| Sesotho    | (nso) |

### Number of Aligned Pairs with Cosine Similarity Score >= 0.65
|src_lang| 	trg_lang| 	num_aligned_pairs| 
|--------|---------|-----------|
|ssw|      	xho|      	2202|
|ssw|      	zul|      	2183|
|xho|      	zul|      	2102|
|nso|      	xho|      	2081|
|nso|      	tso|      	2071|
|ssw|      	tso|      	2034|
|nso|      	ssw|      	2021|
|tsn|      	tso|      	2020|
|tsn|      	xho|      	2009|
|tso|      	xho|      	2009|
|nso|      	tsn|      	2002|
|ssw|      	tsn|      	1987|
|tso|      	zul|      	1957|
|nso|      	zul|      	1953|
|tsn|      	zul|      	1933|
|eng|      	zul|      	1923|
|eng|      	tso|      	1923|
|eng|      	nso|      	1867|
|eng|      	ssw|      	1821|
|afr|      	xho|      	1816|
|eng|      	xho|      	1801|
|nbl|      	sep|      	1795|
|sep|      	ven|      	1794|
|afr|      	ssw|      	1783|
|eng|      	tsn|      	1772|
|afr|      	zul|      	1769|
|afr|      	nso|      	1746|
|nbl|      	ven|      	1699|
|afr|      	eng|      	1661|
|afr|      	tsn|      	1631|
|afr|      	tso|      	1617|
|afr|      	sep|      	551|
|afr|      	ven|      	498|
|afr|      	nbl|      	491|
|nso|      	sep|      	410|
|nso|      	ven|      	352|
|sep|      	tso|      	326|
|sep|      	tsn|      	319|
|tso|      	ven|      	307|
|sep|      	ssw|      	305|
|sep|      	xho|      	300|
|ssw|      	ven|      	290|
|tsn|      	ven|      	285|
|nbl|      	ssw|      	282|
|nbl|      	nso|      	266|
|ven|      	xho|      	260|
|eng|      	sep|      	258|
|nbl|      	xho|      	250|
|sep|      	zul|      	249|
|nbl|      	tso|      	238|
|eng|      	ven|      	234|
|nbl|      	tsn|      	230|
|nbl|      	zul|      	226|
|ven|      	zul|      	225|
|eng|      	nbl|      	184|



The dataset is present in several forms on the repo. 
Generally the dataset is split by edition, eg. `2020-01-ed1`  
The data directory is broken down as follows
```
./data
├── external                # Data external to this repo
├── interim                 # I am not really sure - looks like interim in regards to processed.
├── processed               # The data from scraping the raw pdfs
├── raw                     # The raw pdfs of the Vuk'uzenzele magazine
├── sentence_align_output   # The output (csv) of the sentence alignment with LASER language encoders
└── simple_align_output     # The output (csv) of a simple one to one sentence alignment
```
The dataset is split by edition in the [data/processed](data/processed/) folder.

Authors
-------
- Vukosi Marivate - [@vukosi](https://twitter.com/vukosi)
- Andani Madodonga
- Daniel Njini
- Richard Lastrucci
- Isheanesu Dzingirai
- Jenalea Rajab

Citation
--------
Preprint/Paper

[Preparing the Vuk'uzenzele and ZA-gov-multilingual South African  multilingual corpora](https://arxiv.org/pdf/2303.03750)

> @article{lastrucci2023preparing,
  title   = {Preparing the Vuk'uzenzele and ZA-gov-multilingual South African multilingual corpora},
  author  = {Richard Lastrucci and Isheanesu Dzingirai and Jenalea Rajab and Andani Madodonga and Matimba Shingange and Daniel Njini and Vukosi Marivate},
  year    = {2023},
  journal = {arXiv preprint arXiv: Arxiv-2303.03750}
}

Dataset

Vukosi Marivate, Andani Madodonga, Daniel Njini, Richard Lastrucci, Isheanesu Dzingirai, Jenalea Rajab. **The Vuk'uzenzele South African Multilingual Corpus**, 2023

> @dataset{marivate_vukosi_2023_7598540,
  author       = {Marivate, Vukosi and
                  Njini, Daniel and
                  Madodonga, Andani and
                  Lastrucci, Richard and
                  Dzingirai, Isheanesu
                  Rajab, Jenalea},
  title        = {The Vuk'uzenzele South African Multilingual Corpus},
  month        = feb,
  year         = 2023,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.7598539},
  url          = {https://doi.org/10.5281/zenodo.7598539}
}

Licences
-------
* License for Data - [CC 4.0 BY](LICENSE.data.md)
* Licence for Code - [MIT License](LICENSE.md)
