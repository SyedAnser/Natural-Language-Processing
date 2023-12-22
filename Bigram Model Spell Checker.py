from collections import Counter
import re
from prettytable import PrettyTable

class BigramSpellChecker:
    def __init__(self, corpus):
        self.bigram_counts = self.calculate_bigram_counts(corpus)
        self.unigram_counts = Counter(corpus)
        self.vocab_size = len(set(corpus))

    def calculate_bigram_counts(self, corpus):
        bigrams = [(word[i:i + 2]) for word in corpus for i in range(len(word) - 1)]
        return Counter(bigrams)

    def get_probability(self, bigram):
        # Laplace smoothing for better handling of unseen bigrams
        return (self.bigram_counts[bigram] + 1) / (self.unigram_counts[bigram[0]] + self.vocab_size)
    
    def get_suggestions(self, misspelled_word):
        suggestions = {}
        for word in set(self.unigram_counts.keys()):
            # Exclude single-letter words and numbers
            if len(word) > 1 and not word.isdigit():
                matching_bigrams = []
                mismatched_bigrams = []
                for i in range(len(misspelled_word) - 1):
                    misspelled_bigram = misspelled_word[i:i + 2]
                    found_match = False
                    for j in range(len(word) - 1):
                        checked_bigram = word[j:j + 2]
                        if misspelled_bigram == checked_bigram:
                            matching_bigrams.append(f"{misspelled_bigram}[{i + 1}] - {checked_bigram}[{j + 1}]")
                            found_match = True
                            break

                    if not found_match:
                        mismatched_bigrams.append(f"{misspelled_bigram}[{i + 1}] - No Match")

                suggestions[word] = (matching_bigrams, mismatched_bigrams)

        sorted_suggestions = sorted(suggestions.items(), key=lambda x: (-len(x[1][0]), x[0]))

        table = PrettyTable()
        table.field_names = ["#", f"Suggestions for '{misspelled_word}'", "Matching Bigrams", "Mismatched Bigrams"]

        for idx, (word, (matching_bigrams, mismatched_bigrams)) in enumerate(sorted_suggestions[:10], start=1):
            bigram_indices = [f"{i + 1}" for i in range(len(matching_bigrams))]
            mismatched_bigram_indices = [f"{i + 1}" for i in range(len(mismatched_bigrams))]
            table.add_row([idx, word, "\n".join(matching_bigrams), "\n".join(mismatched_bigrams)])

            # Add a line between entries
            table.add_row(["---", "---", "---", "---"])

        # Remove the last line
        table.del_row(-1)

        print(table)

        return [word for word, _ in sorted_suggestions[:10]]




    
# Example usage
corpus = """
Natural language processing (NLP) is a field of artificial intelligence that focuses on the interaction between computers and humans using natural language. 
It involves the development of algorithms and models that enable computers to understand, interpret, and generate human-like text. 
NLP has a wide range of applications, including machine translation, sentiment analysis, chatbots, and spell checking.
In recent years, NLP has seen significant advancements, thanks to deep learning techniques and large datasets for example. 
These advancements have led to the development of powerful language models like GPT-3, 
which can perform a variety of language-related tasks with remarkable accuracy. 
However, spell checking remains a fundamental aspect of NLP, ensuring that written text is free from spelling errors.
A bigram spell checker is one approach to address spelling issues. By considering the probabilities of adjacent word pairs (bigrams), 
it can suggest corrections for misspelled words. This simple implementation uses a toy dataset, but in real-world scenarios, 
a more extensive corpus would be required for better accuracy.
To enhance the spell checker, you can explore incorporating more sophisticated language models, handling unseen words more effectively, 
and considering higher-order n-grams. 
Additionally, using pre-trained language models or fine-tuning them on domain-specific data can improve the spell checker's performance.
In conclusion, spell checking remains a crucial component of natural language processing, ensuring that written communication is accurate and error-free.
As technology continues to advance, we can expect further improvements in spell checking algorithms and their integration into various applications.
"""

# Preprocess the longer corpus
longer_corpus = re.findall(r'\b\w+\b', corpus.lower())

# Use the longer corpus for the spell checker
spell_checker_longer_corpus = BigramSpellChecker(longer_corpus)

# Example usage with a misspelled input text
misspelled_word = "checkre"

suggestions = spell_checker_longer_corpus.get_suggestions(misspelled_word)
print(f"Suggestions for '{misspelled_word}': {suggestions}")
