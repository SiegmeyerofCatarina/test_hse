# test task for perm-itnetwork
# script for keywords extraction

from os import path
import sys
import re
from collections import Counter
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
import pandas as pd

# text reading, cleaning and splitting into words
if len(sys.argv) > 1:
    if path.exists(sys.argv[1]):
        with open(sys.argv[1]) as f:
            text = re.split(r'\b[\W\d\s]+\b', f.read())
    else:
        raise FileNotFoundError("File {} not found".format(sys.argv[1]))
else:
    raise Exception("Missing commad line parameter")

# word normalization      
morph = MorphAnalyzer()
normal_words = [morph.parse(word)[0].normal_form for word in text]        
        
# stopwords removing
try:
    set_stopwords = set(stopwords.words('russian'))
except Exception:
    import nltk
    nltk.download('stopwords')
    set_stopwords = set(stopwords.words('russian'))
    
set_words = set(normal_words) - set_stopwords

# Words counting and sorting
counted_words = pd.Series(Counter(normal_words))
sorted_words = counted_words[set_words].sort_values(ascending=False)

# Assignment keywords
keywords = sorted_words > sorted_words[0]/3

# Save
csv_path = path.splitext(sys.argv[1])[0] + "_keywords.csv"
sorted_words[keywords].to_csv(csv_path, header=False )

print("Done! Extracted {} keywords. Results saved in {}".format(keywords.sum(), csv_path))
