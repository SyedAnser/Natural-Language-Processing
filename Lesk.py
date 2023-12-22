# Analysis:
# Original Lesk has a higher rate of successful WSD but is slower
# Simplified Lesk is faster has a lower accuracy


import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import time

# Sample sentence for word sense disambiguation
context = "He swung the bat and hit the ball out of the park."
target_word = "bat"

def simplified_lesk_algorithm(word, ctxt):
    best_sns = None
    max_ovlp = 0

    # Tokenize the context
    ctxt_words = set(word_tokenize(ctxt.lower()))

    # Get synsets of the target word
    tgt_synsets = wordnet.synsets(word)

    for sns in tgt_synsets:
        # Get the definition of the sense
        sns_def = set(word_tokenize(sns.definition().lower()))

        # Calculate the overlap between context and sense definition
        ovlp = len(ctxt_words.intersection(sns_def))

        # Update the best sense if the overlap is greater
        if ovlp > max_ovlp:
            max_ovlp = ovlp
            best_sns = sns

    return best_sns

def lesk_algorithm(word, ctxt):
    best_sns = None
    max_ovlp = 0

    # Tokenize the context
    ctxt_words = set(word_tokenize(ctxt.lower()))

    # Get synsets of the target word
    tgt_synsets = wordnet.synsets(word)

    for sns in tgt_synsets:
        # Get the definition and examples of the sense
        sns_def = set(word_tokenize(sns.definition().lower()))
        sns_ex = set(word_tokenize(sns.examples()[0].lower())) if sns.examples() else set()

        # Calculate the overlap between context and sense definition/examples
        ovlp = len(ctxt_words.intersection(sns_def)) + len(ctxt_words.intersection(sns_ex))

        # Update the best sense if the overlap is greater
        if ovlp > max_ovlp:
            max_ovlp = ovlp
            best_sns = sns

    return best_sns


# Measure the time taken for the Original Lesk algorithm
start_time = time.time()
lesk_sns = lesk_algorithm(target_word, context)
end_time = time.time()

if lesk_sns:
    print("\nOriginal Lesk:\n")
    print("Target Word:", target_word)
    print("Context:", context)
    print("Best Sense:", lesk_sns.name(), "-", lesk_sns.definition())
else:
    print("Original Lesk: No sense found for the target word in the given context.")

print("Time taken for Original Lesk algorithm:", end_time - start_time, "seconds\n\n")

# Measure the time taken for the Simplified Lesk algorithm
start_time = time.time()
simplified_lesk_sns = simplified_lesk_algorithm(target_word, context)
end_time = time.time()

if simplified_lesk_sns:
    print("Simplified Lesk:\n")
    print("Target Word:", target_word)
    print("Context:", context)
    print("Best Sense:", simplified_lesk_sns.name(), "-", simplified_lesk_sns.definition())
else:
    print("Simplified Lesk: No sense found for the target word in the given context.")

print("Time taken for Simplified Lesk algorithm:", end_time - start_time, "seconds")


