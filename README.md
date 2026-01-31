# USE24-XD (U.S. Election 2024 X.com Dataset)

This dataset comprises nearly **100,000** social media posts from X.com (formerly Twitter), collected between **October 17, 2024**, and **July 16, 2025**. The data span the pre- and post-election periods of the 2024 U.S. presidential race. Posts were selected if they mention both “election” and “2024” and include metadata such as engagement, location, and sentiment. Each post is annotated with five harmful content multi-labels predicted by six large language models. A subset of posts was also evaluated by human annotators.


## Metadata
- `created_at` — Timestamp when the post was created.  
- `id` — Unique identifier for the tweet.  
- `author_id` — Unique identifier for the tweet’s author.  
- `username` — The handle of the tweet’s author.  
- `name` — Display name of the author.  
- `verified` — Boolean indicating whether the author’s account is verified.  
- `possibly_sensitive` — Boolean flag for sensitive media content.  
- `lang` — Language of the tweet.  
- `edit_history_tweet_ids` — IDs tracking edits of the tweet.  

## Text Content
- `text` — Raw tweet text.  
- `clean_text` — Preprocessed version of the tweet text (cleaned for analysis).  
- `word_count` — Number of words in the cleaned text.  
- `hashtags` — Extracted hashtags used in the tweet.  
- `entities.mentions` — User mentions present in the tweet.  

## Location Information
- `user_location` — Free-text user-provided location.  
- `user_location_USA_state` — Parsed U.S. state if the location is identifiable.  

## Engagement Metrics
- `public_metrics.retweet_count` — Number of retweets.  
- `public_metrics.reply_count` — Number of replies.  
- `public_metrics.like_count` — Number of likes.  
- `public_metrics.quote_count` — Number of quote tweets.  
- `public_metrics.bookmark_count` — Number of bookmarks.  
- `public_metrics.impression_count` — Number of impressions.  

## Sentiment Analysis
- `sentiment_vader_raw` — Continuous VADER sentiment score.  
- `sentiment_vader_label` — Categorical sentiment label (positive, neutral, negative).  

## LLM-Based Annotations
Each model predicts whether a tweet belongs to one or more of five categories: **Conspiracy, Sensationalism, Hate Speech, Speculation, Satire**. Columns are binary indicators (1 = present/True, 0 = absent/False).  

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


## Notes and Limitations
- Dataset relies on the **basic-tier streaming API**
- Geographic analysis should be interpreted with caution because locations are **self-reported** by users
- For access to the complete dataset, please contact **kylewang@udel.edu**

## Citation
If you use this dataset in your research, please cite it as: TBD

## License  
This project is licensed under the MIT License - see the [LICENSE.md](./LICENSE)  file for details


#api #computerScience #application #machineLearning #supervisedLearning #unsupervisedLearning #classification #dataset #llms #chatgpt #OpenData #ResearchDataset #DataScience #ComputationalSocialScience #LLMResearch #SocialMediaAnalysis #AIAnnotation #HumanAICollaboration #AIResearch #NLPResearch #Election2024 #PoliticalDiscourse #Misinformation #MediaBias #Democracy #SocialMediaPolitics #AcademicTwitter #OpenScience #HCIResearch #PoliticalScience #DigitalSociety #WisdomOfCrowd
