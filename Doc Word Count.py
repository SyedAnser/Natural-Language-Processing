import string
import nltk
from nltk.corpus import stopwords
from collections import Counter


def with_punctuation(filename):
    with open(filename, 'r') as file:
        text = file.read().lower()  
    
    
    for punctuation in string.punctuation:
        text = text.replace(punctuation, f' {punctuation} ')
    
    
    words = text.split()
    
   
    unique_words = set(words)

    word_frequencies = Counter(words)
    
   
    unique_word_frequencies = {word: freq for word, freq in word_frequencies.items() if word in unique_words}
    
    return unique_word_frequencies


def no_punctuation(filename):
    with open(filename, 'r') as file:
        text = file.read().lower()  
    

    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)
    
    
    words = text.split()
    
  
    unique_words = set(words)
    
    word_frequencies = Counter(words)
    
    
    unique_word_frequencies = {word: freq for word, freq in word_frequencies.items() if word in unique_words}
    
    return unique_word_frequencies


def no_punc_stopwords(filename):
    with open(filename, 'r') as file:
        text = file.read().lower()  
    
   
    for punctuation in string.punctuation:
        text = text.replace(punctuation, ' ')
    
    
    words = text.split()
    
    
    unique_words = set(words)
    
   
    stop_words = set(stopwords.words('english'))
    
    
    filtered_unique_words = unique_words - stop_words

    word_frequencies = Counter(words)
    
   
    unique_word_frequencies = {word: freq for word, freq in word_frequencies.items() if word in filtered_unique_words}
    
    return unique_word_frequencies

    

filename = 'C:/Users/syeda/OneDrive/Desktop/codes/text1.txt'



word_frequencies = with_punctuation(filename)

total_unique_words = len(word_frequencies)

print(f"\nTotal Unique Words with punctuation: {total_unique_words}\n")

for word, frequency in word_frequencies.items():
    print(f"{word}: {frequency}")



word_frequencies = no_punctuation(filename)

total_unique_words = len(word_frequencies)

print(f"\nTotal Unique Words without punctuation: {total_unique_words}\n")

for word, frequency in word_frequencies.items():
    print(f"{word}: {frequency}")



word_frequencies = no_punc_stopwords(filename)

print(f"\n\nTotal Unique Words (excluding punctuation and stop words): {len(word_frequencies)}\n")

for word, frequency in word_frequencies.items():
    print(f"{word}: {frequency}")

