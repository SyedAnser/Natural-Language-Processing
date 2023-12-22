import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import words

english_words = set(words.words())


class CustomPorterStemmer(PorterStemmer):
    def stem(self, word):
        stem = super().stem(word)
        
        if word.endswith('ying') and stem.endswith('y'):
            stem=stem
        elif word.endswith("ing") and stem.endswith("ing") and len(stem) > 4:
            stem = stem[:-3]
        elif word.endswith("ing") and stem not in english_words :
            stem=stem+'e'
        if word.endswith("e") and len(stem) > 3:
            stem = word 
        if word.endswith("s") and len(stem) <= 3:
            stem = word  
        if word.endswith("ion") and stem.endswith("ion") and len(stem) > 4:
            stem = stem[:-3]+'e'  
        if word.endswith('ity'):
            stem+='e'
            if stem.endswith('ive'):
                stem=stem[:-3]+'e'
        if word.endswith('ive') and stem.endswith('ive'):
            stem=stem[:-3]
        if stem.endswith('i') and len(word)>5:
            stem=stem[:-1]+'y'
        if word.endswith('ly') and stem.endswith('ly') or stem.endswith('li') and len(stem)>=3:
            stem=stem[:-2]
            if stem.endswith('i') and len(word)>5:
                stem=stem[:-1]+'y'
        
        return stem

# Example words
words = input("enter word:")
stemmer = CustomPorterStemmer()

stemmed_word = stemmer.stem(words)

print("Original Word:", words)
print("Stemmed Word:", stemmed_word)
print()
