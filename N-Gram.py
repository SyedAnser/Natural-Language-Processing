import string
import nltk
from collections import Counter
from tabulate import tabulate

# Sample training corpus
corpus = "Hello. Fun times! How is the weather?"

# Preprocess the corpus
translator = str.maketrans('', '', string.punctuation.replace('.', '').replace('!', '').replace('?', ''))
corpus = corpus.translate(translator)
sentences = nltk.sent_tokenize(corpus)
words = [nltk.word_tokenize(sentence) for sentence in sentences]

# Calculate unigram and bigram frequencies
unigrams = [word for sentence in words for word in sentence]
bigrams = [(prev_word, word) for sentence in words for prev_word, word in zip(sentence, sentence[1:])]

unigram_freq = Counter(unigrams)
bigram_freq = Counter(bigrams)


# Create a vocabulary for both unigrams and bigrams
vocab_unigrams = sorted(list(set(unigrams)))

# Create a bigram matrix for unsmoothed model with row and column headers
unsmoothed_bigram_matrix = [[""] + vocab_unigrams]
for prev_word in vocab_unigrams:
    row = [prev_word]
    for word in vocab_unigrams:
        if (prev_word, word) in bigram_freq:
            row.append(str(bigram_freq[(prev_word, word)]))
        else:
            row.append("0")
    unsmoothed_bigram_matrix.append(row)

# Create a bigram matrix for smoothed model with row and column headers
V_bigram = len(vocab_unigrams)
smoothed_bigram_matrix = [[""] + vocab_unigrams]
for prev_word in vocab_unigrams:
    row = [prev_word]
    for word in vocab_unigrams:
        if (prev_word, word) in bigram_freq:
            row.append(f"{(bigram_freq[(prev_word, word)] + 1) / (unigram_freq[prev_word] + V_bigram):.4f}")
        else:
            row.append(f"{1 / (unigram_freq[prev_word] + V_bigram):.4f}")
    smoothed_bigram_matrix.append(row)

# Print the bigram matrix for unsmoothed model with headers using tabulate
headers = unsmoothed_bigram_matrix[0]
table = unsmoothed_bigram_matrix[1:]
unsmoothed_table = tabulate(table, headers=headers, tablefmt="grid")

total_unigrams = len(unigrams)
total_bigrams = len(bigrams)

unigram_probs = {word: freq / total_unigrams for word, freq in unigram_freq.items()}
bigram_probs = {(prev_word, word): freq / total_bigrams for (prev_word, word), freq in bigram_freq.items()}

# Apply Add-One (Laplace) smoothing to both unigrams and bigrams
V_unigram = len(set(unigrams))
V_bigram = len(set(bigrams))


smoothed_unigram_probs = {word: (freq + 1) / (total_unigrams + V_unigram) for word, freq in unigram_freq.items()}
smoothed_bigram_probs = {(prev_word, word): (freq + 1) / (bigram_freq[(prev_word, word)] + V_bigram) for (prev_word, word), freq in bigram_freq.items()}

sorted_unigrams = sorted(unigram_probs.items(), key=lambda x: x[1], reverse=True)
sorted_bigrams = sorted(bigram_probs.items(), key=lambda x: x[1], reverse=True)

sorted_smoothed_unigrams = sorted(smoothed_unigram_probs.items(), key=lambda x: x[1], reverse=True)
sorted_smoothed_bigrams = sorted(smoothed_bigram_probs.items(), key=lambda x: x[1], reverse=True)

# Print the bigram matrix for smoothed model with headers using tabulate
headers = smoothed_bigram_matrix[0]
table = smoothed_bigram_matrix[1:]
smoothed_table = tabulate(table, headers=headers, tablefmt="grid")

print("Unigram (Unsmoothed)".ljust(30), "Count".ljust(10), "Probability")
for word, prob in sorted_unigrams:
    print(word.ljust(30), str(unigram_freq[word]).ljust(10), f"{prob:.4f}")

print("\nBigram (Unsmoothed)".ljust(40), "Count".ljust(10), "Probability")
for (prev_word, word), prob in sorted_bigrams:
    print(f"{prev_word} {word}".ljust(40), str(bigram_freq[(prev_word, word)]).ljust(10), f"{prob:.4f}")

print("\nUnigram (Smoothed)".ljust(30), "Count".ljust(10), "Probability")
for word, prob in sorted_smoothed_unigrams:
    print(word.ljust(30), str(unigram_freq[word]).ljust(10), f"{prob:.4f}")

print("\nBigram (Smoothed)".ljust(40), "Count".ljust(10), "Probability")
for (prev_word, word), prob in sorted_smoothed_bigrams:
    print(f"{prev_word} {word}".ljust(40), str(bigram_freq[(prev_word, word)]).ljust(10), f"{prob:.4f}")
          
print("Bigram Probability Matrix (Unsmoothed):")
print(unsmoothed_table)

print("\nBigram Probability Matrix (Smoothed):")
print(smoothed_table)



