# U.S. Election 2024 X.com Dataset (USE24-XD)
This dataset comprises nearly **100,000** public posts from X.com (formerly Twitter), collected between **October 17, 2024** and **July 16, 2025**. The data span both the pre- and post-election periods of the 2024 U.S. presidential race. Posts were selected if they mention both *“election”* and *“2024”* and include metadata such as engagement signals, location indicators, and sentiment scores.

Each post is annotated with five harmful content multi-labels generated using an ensemble of six large language models (LLMs). A subset of posts was also evaluated by human annotators to support validation and comparison.

![plot](Figures/overall_flow.jpg)
*Figure 1. Overall workflow of the USE24-XD annotation pipeline.*


## Citation
If you use this dataset in your research, please cite:

*TBD*


 # 📄 [U.S_Election_2024_Xcom_Dataset.csv](U.S_Election_2024_Xcom_Dataset.csv)


### 👉 [Check out sample dataset](U.S_Election_2024_Xcom_Dataset_Sample100.csv)

## Text Content
- `id` — Unique identifier for the post  
- `created_at` — Timestamp when the post was created  
- `text` — Raw post text  
- `text_clean` — Preprocessed text used for analysis  
- `word_count` — Number of words in the cleaned text  
- `hashtags` — Extracted hashtags  
- `entities.mentions` — User mentions within the post  


## Metadata
- `author_id` — Unique identifier for the author  
- `username` — [Redacted for privacy reasons]  
- `name` — Display name of the author  
- `verified` — Whether the account is verified  
- `possibly_sensitive` — Flag for sensitive media content  
- `lang` — Detected language  
- `edit_history_tweet_ids` — Edit history identifiers  


## Location Information

- `user_location` — Free-text self-reported location  
- `user_location_USA_state` — Parsed U.S. state when identifiable  



## Engagement Metrics

- `public_metrics.retweet_count` — Number of Retweets  
- `public_metrics.reply_count` — Number of Replies  
- `public_metrics.like_count` — Number of Likes  
- `public_metrics.quote_count` — Number of Quote Posts  
- `public_metrics.bookmark_count` — Number of Bookmarks  
- `public_metrics.impression_count` — Number of Impressions  



## Sentiment Analysis

- `sentiment_vader_raw` — Continuous VADER sentiment score  
- `sentiment_vader_label` — Categorical sentiment label (`positive`, `neutral`, `negative`)  



## LLM-Based Annotations

Using a wisdom-of-the-crowd aggregation approach that combines the best-performing LLM outputs alongside human evaluation, we curate a robust multi-label dataset across five categories Columns are binary indicators (`1 = present`, `0 = absent`):

- `Speculation`
- `Sensationalism` 
- `Conspiracy`
- `Hate_Speech`
- `Satire` 

![plot](Figures/concurrent_labels.jpg)
*Figure 2. Distribution of multi-label annotations across five harmful content categories with intersection sizes and marginal
frequencies of each label



# Intermediary Data Files


## 📄 [LLM_Individual_Annotation.csv](Intermediary/LLM_Individual_Annotation.csv)

Each model predicts whether a post belongs to one or more of five categories: **Conspiracy, Sensationalism, Hate Speech, Speculation, Satire**. Columns are binary indicators (`1 = present`, `0 = absent`).

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



## 📄 [Human_Annotation_Subset.csv](Intermediary/Human_Annotation_Subset.csv)

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
- For questions, contact: **kylewang@udel.edu**


## License

This project is licensed under the MIT License. See [LICENSE.md](./LICENSE) for details.
