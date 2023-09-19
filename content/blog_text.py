import requests
import pandas as pd
from rake_nltk import Rake
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk import pos_tag

#  download tagger
nltk.download('averaged_perceptron_tagger')

# Keyword Extracter

class KeywordExplorer():

    def __init__(self, text, num_keywords):
        
        self.text = text
        self.num_keywords = num_keywords
        
    def extract_single_keywords(self):
        
        tokens = word_tokenize(self.text)
        tokens = [word.lower() for word in tokens if word.isalnum()]

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]

        # Perform Part-of-Speech tagging
        tagged_tokens = pos_tag(filtered_tokens)

        # Extract nouns and adjectives as keywords
        keywords = [word for word, pos in tagged_tokens if pos.startswith('N') or pos.startswith('J')]

        # Calculate word frequency
        fdist = FreqDist(keywords)

        # Get the most common keywords
        top_keywords = fdist.most_common(self.num_keywords)
        keywords_df = pd.DataFrame(top_keywords, columns=['Keyword', 'Frequency'])

        return keywords_df

    def extract_two_tail_keywords(self):

        r = Rake(min_length=2, max_length=2)

        # Extract keywords from the text
        r.extract_keywords_from_text(self.text)

        # Get the ranked keywords
        keywords = r.get_ranked_phrases_with_scores()
        phrase_counts = {}

        # Iterate through the keywords and update the counts
        for score, phrase in keywords:
            if phrase in phrase_counts:
                phrase_counts[phrase] += 1
            else:
                phrase_counts[phrase] = 1

        # Sort the phrases in descending order of counts
        sorted_phrases = sorted(phrase_counts.items(), key=lambda x: x[1], reverse=True)
        
        bigrams_df = pd.DataFrame(sorted_phrases, columns=['Bigram', 'Frequency'])
  
        return bigrams_df
    
        