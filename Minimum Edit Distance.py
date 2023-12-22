import nltk
from nltk.util import ngrams

# Sample strings
str1 = "kitten"
str2 = "sitting"

# Define a function to generate N-grams
def generate_ngrams(text, n):
    # Convert the string to a list of characters for character-based n-grams
    tokens = list(text)
    n_grams = list(ngrams(tokens, n))
    return n_grams

# Example of generating N-grams
n = 3  # You can adjust the value of 'n' for different N-grams
str1_ngrams = generate_ngrams(str1, n)
str2_ngrams = generate_ngrams(str2, n)

print(f"{n}-grams for '{str1}': {str1_ngrams}")
print(f"{n}-grams for '{str2}': {str2_ngrams}")

# Calculate Minimum Edit Distance
med = nltk.edit_distance(str1, str2)
print(f"Minimum Edit Distance between '{str1}' and '{str2}': {med}")
