# U.S. Election 2024 X.com Dataset (USE24-XD)

[![arXiv](https://img.shields.io/badge/arXiv-2602.11962-B31B1B?logo=arxiv&logoColor=white)](https://arxiv.org/abs/2602.11962)
[![Zenodo](https://img.shields.io/badge/Zenodo-21970648-1682D4?logo=zenodo&logoColor=white)](https://zenodo.org/records/21970648)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This release contains **97,696 dehydrated public posts** from X.com (formerly Twitter), collected between **October 17, 2024** and **July 16, 2025**. The data span both the pre- and post-election periods of the 2024 U.S. presidential race. Posts were selected if they mention both *“election”* and *“2024”*.

The released file omits post text and direct account or engagement metadata. It retains post IDs, selected derived features, and five harmful-content labels generated with an ensemble of six large language models (LLMs). A subset of posts was also evaluated by human annotators to support validation and comparison.

![plot](Figures/overall_flow.jpg)
*Figure 1. Overall workflow of the USE24-XD annotation pipeline*.

## Complete dataset

The complete dataset may be requested from the [Zenodo record](https://zenodo.org/records/21970648).

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21970648.svg)](https://doi.org/10.5281/zenodo.21970648)

## Dataset files



### 📄 [U.S_Election_2024_Xcom_Dataset_Dehydrated.csv](U.S_Election_2024_Xcom_Dataset_Dehydrated.csv)

The primary dataset contains 97,696 post IDs with selected derived features and aggregated labels.

### 🔎 Preview: [U.S_Election_2024_Xcom_Dataset_Dehydrated_sample100.csv](U.S_Election_2024_Xcom_Dataset_Dehydrated_sample100.csv)

The preview contains 100 randomly sampled rows.

### Dehydrated dataset schema

- `id` — Unique identifier for the post
- `word_count` — Number of words in the original text
- `hashtag` — Extracted hashtags
- `user_location_usa_state` — Parsed U.S. state, when identifiable from self-reported location
- `sentiment_score` — Continuous VADER sentiment score
- `sentiment_label` — Categorical sentiment label (`positive`, `neutral`, or `negative`)

### Aggregated harmful-content labels

Using a wisdom-of-the-crowd aggregation approach that combines the best-performing LLM outputs alongside human evaluation, we curate a robust multi-label dataset across five categories. The following columns are binary indicators (`1 = present`, `0 = absent`):

- `Speculation`
- `Sensation` (sensationalism)
- `conspiracy`
- `hate_speech`
- `Satire`

### Rehydration

The dataset includes post IDs for researchers who are permitted to rehydrate records. Availability of individual posts is not guaranteed; any rehydration and use of X.com data must comply with the platform’s current policies and terms.

![plot](Figures/concurrent_labels.jpg)
*Figure 2. Distribution of multi-label annotations across five harmful content categories with intersection sizes and marginal frequencies of each label*.



## Intermediary data files


### 📄 [LLM_Individual_Annotation.csv](Intermediary/LLM_Individual_Annotation.csv)

This file contains individual predictions for all 97,696 posts. Each model predicts whether a post belongs to one or more of five categories: **Conspiracy, Sensationalism, Hate Speech, Speculation, Satire**. Columns are binary indicators (`1 = present`, `0 = absent`).

### 🔎 Checkout preview: [LLM_Individual_Annotation_Sample100.csv](Intermediary/LLM_Individual_Annotation_Sample100.csv)


- `id` — Unique identifier for the post  

### GPT-4o Mini
- `Conspiracy_gpt4o_mini`
- `Sensationalism_gpt4o_mini`
- `Hate_Speech_gpt4o_mini`
- `Speculation_gpt4o_mini`
- `Satire_gpt4o_mini`

### GPT-4o
- `Conspiracy_gpt4o`
- `Sensationalism_gpt4o`
- `Hate_Speech_gpt4o`
- `Speculation_gpt4o`
- `Satire_gpt4o`

### Gemini 2.0 Flash
- `Conspiracy_gemini_2.0_flash`
- `Sensationalism_gemini_2.0_flash`
- `Hate_Speech_gemini_2.0_flash`
- `Speculation_gemini_2.0_flash`
- `Satire_gemini_2.0_flash`

### Gemini 2.5 Pro
- `Conspiracy_gemini_2.5_pro`
- `Sensationalism_gemini_2.5_pro`
- `Hate_Speech_gemini_2.5_pro`
- `Speculation_gemini_2.5_pro`
- `Satire_gemini_2.5_pro`

### Llama 3.1 (8B)
- `Conspiracy_llama3.1_8B`
- `Sensationalism_llama3.1_8B`
- `Hate_Speech_llama3.1_8B`
- `Speculation_llama3.1_8B`
- `Satire_llama3.1_8B`

### Llama 3.3 (70B)
- `Conspiracy_llama3.3`
- `Sensationalism_llama3.3`
- `Hate_Speech_llama3.3`
- `Speculation_llama3.3`
- `Satire_llama3.3`



### 📄 [Human_Annotation_Subset.csv](Intermediary/Human_Annotation_Subset.csv)

A random sample of **1,000 posts (≈1%)** was annotated by three human annotators. The file includes individual annotations as well as majority-vote labels. Columns are binary indicators (`1 = present`, `0 = absent`)

Columns include:

- `id`  — Unique identifier for the post
- `conspiracy_majority`
- `hate_speech_majority`
- `satire_majority`
- `sensationalism_majority`
- `speculation_majority`

Individual annotations:
- `conspiracy1`, `conspiracy2`, `conspiracy3`
- `hate_speech1`, `hate_speech2`, `hate_speech3`
- `satire1`, `satire2`, `satire3`
- `sensationalism1`, `sensationalism2`, `sensationalism3`
- `speculation1`, `speculation2`, `speculation3`

## Notes and Limitations

- Data were collected using the **basic-tier streaming API**  
- Geographic analysis should be interpreted cautiously because locations are **self-reported**  
- Released records are dehydrated; post availability may change over time.
- For questions, contact: **kylewang@udel.edu**


## Citation
For the accompanying paper, please cite:

Wang, Q., Khatiwada, P., Vieira, C. C., Bagozzi, B. E., Barner, K. E., & Mauriello, M. L. (2026). *Wisdom of the LLM Crowd: A Large Scale Benchmark of Multi-Label US Election-Related Harmful Social Media Content*. arXiv preprint arXiv:2602.11962.

```bibtex
@article{wang2026wisdom,
  title={Wisdom of the LLM Crowd: A Large Scale Benchmark of Multi-Label US Election-Related Harmful Social Media Content},
  author={Wang, Qile and Khatiwada, Prerana and Vieira, Carolina Coimbra and Bagozzi, Benjamin E and Barner, Kenneth E and Mauriello, Matthew Louis},
  journal={arXiv preprint arXiv:2602.11962},
  year={2026}
}
```

For the dataset, please cite:

Wang, Q., Khatiwada, P., Coimbra Vieira, C., Bagozzi, B., Barner, K., & Mauriello, M. L. (2026). A multi-label dataset of large language model and crowd annotated U.S. 2024 election X (Twitter) posts for harmful content research [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.21970648

```bibtex
@dataset{wang_2026_21970648,
  author = {Wang, Qile and Khatiwada, Prerana and Coimbra Vieira, Carolina and Bagozzi, Benjamin and Barner, Kenneth and Mauriello, Matthew Louis},
  title  = {A multi-label dataset of large language model and crowd annotated U.S. 2024 election X (Twitter) posts for harmful content research},
  month  = aug,
  year   = 2026,
  publisher    = {Zenodo},
  doi    = {10.5281/zenodo.21970648},
  url    = {https://doi.org/10.5281/zenodo.21970648},
}
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
