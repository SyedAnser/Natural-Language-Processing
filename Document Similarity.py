import nltk
import spacy
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.corpus import wordnet

tfidf_vectorizer = TfidfVectorizer()
stop_words = set(stopwords.words('english'))
nlp = spacy.load("en_core_web_sm")

with open("C:/Users/syeda/OneDrive/Desktop/codes/NLP/txt1.txt",'r') as f1:
    document1=f1.read()
with open("C:/Users/syeda/OneDrive/Desktop/codes/NLP/txt2.txt", 'r') as f2:
    document2=f2.read()

tokens1 = word_tokenize(document1)
tokens2 = word_tokenize(document2)
filtered_tokens1 = [word for word in tokens1 if word.lower() not in stop_words]
filtered_tokens2 = [word for word in tokens2 if word.lower() not in stop_words]

def sim_check():
    combined_tokens = [" ".join(tokens1), " ".join(tokens2)]

    tfidf_matrix = tfidf_vectorizer.fit_transform(combined_tokens)

    cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

    print(f"Cosine Similarity: {cosine_sim[0][0]}")


def sim_check_wo_stop_word():
    combined_tokens = [" ".join(filtered_tokens1), " ".join(filtered_tokens2)]

    tfidf_matrix = tfidf_vectorizer.fit_transform(combined_tokens)

    cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

    print(f"Cosine Similarity (without stop words): {cosine_sim[0][0]}")


def syn_sim_check():
    def get_synonyms(word):
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
        return list(synonyms)

    expanded_tokens1 = [get_synonyms(word) + [word] for word in filtered_tokens1]
    expanded_tokens2 = [get_synonyms(word) + [word] for word in filtered_tokens2]

    # Convert expanded tokens back to strings
    expanded_text1 = " ".join([word for sublist in expanded_tokens1 for word in sublist])
    expanded_text2 = " ".join([word for sublist in expanded_tokens2 for word in sublist])

    # Combine expanded text into a single list for TF-IDF vectorization
    combined_expanded_text = [expanded_text1, expanded_text2]

    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Fit and transform the documents
    tfidf_matrix = tfidf_vectorizer.fit_transform(combined_expanded_text)

    # Calculate cosine similarity between the two documents
    cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

    # Print the cosine similarity score
    print(f"Cosine Similarity (with synonyms and without stop words): {cosine_sim[0][0]}")


def morph_sim_check():
    def get_lemmas(word):
        lemmatizer = WordNetLemmatizer()
        return lemmatizer.lemmatize(word)
    
    lemmatized_tokens1 = [get_lemmas(word) for word in filtered_tokens1]
    lemmatized_tokens2 = [get_lemmas(word) for word in filtered_tokens2]

    # Convert lemmatized tokens back to strings
    lemmatized_text1 = " ".join(lemmatized_tokens1)
    lemmatized_text2 = " ".join(lemmatized_tokens2)

    # Combine lemmatized text into a single list for TF-IDF vectorization
    combined_lemmatized_text = [lemmatized_text1, lemmatized_text2]

    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Fit and transform the documents
    tfidf_matrix = tfidf_vectorizer.fit_transform(combined_lemmatized_text)

    # Calculate cosine similarity between the two documents
    cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

    # Print the cosine similarity score
    print(f"Cosine Similarity (with lemmatization and without stop words): {cosine_sim[0][0]}")

def ngram_sim_check():
    def create_ngrams(text, n):
        doc = nlp(text)
        tokens = [token.text for token in doc]
        ngrams = [tokens[i:i+n] for i in range(len(tokens)-n+1)]
        return [' '.join(ngram) for ngram in ngrams]

    # Prompt the user for the value of 'n'
    n = int(input("Enter the value of 'n' for n-grams: "))

    # Create n-grams from the text documents
    ngrams1 = create_ngrams(document1, n)
    ngrams2 = create_ngrams(document2, n)

    # Convert n-grams back to strings
    ngrams_text1 = ' '.join(ngrams1)
    ngrams_text2 = ' '.join(ngrams2)

    # Combine n-grams text into a single list for TF-IDF vectorization
    combined_ngrams_text = [ngrams_text1, ngrams_text2]

    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Fit and transform the documents
    tfidf_matrix = tfidf_vectorizer.fit_transform(combined_ngrams_text)

    # Calculate cosine similarity between the two documents based on n-grams
    cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

    # Print the cosine similarity score
    print(f"Cosine Similarity (with {n}-grams): {cosine_sim[0][0]}")


def frame_check():
    def create_frames(text, frame_length):
        doc = nlp(text)
        tokens = [token.text for token in doc]
        frames = [tokens[i:i+frame_length] for i in range(0, len(tokens), frame_length)]
        return [' '.join(frame) for frame in frames]

    # Specify the frame length
    frame_length = int(input("Enter frame size="))  # Adjust the frame length as needed

    # Create frames from the text documents
    frames1 = create_frames(document1, frame_length)
    frames2 = create_frames(document2, frame_length)

    # Combine frames into a single list for TF-IDF vectorization
    identical_frames = sum(1 for frame1 in frames1 for frame2 in frames2 if frame1 == frame2)

    # Calculate the total number of frames
    total_frames = len(frames1) + len(frames2)  # Use addition, not multiplication

    # Calculate the ratio of identical frames to total frames
    identical_ratio = identical_frames / total_frames

    # Print the results
    print(f"Number of Identical Frames: {identical_frames}")
    print(f"Total Frames: {total_frames}")
    print(f"Identical Frames Ratio: {identical_ratio}")

sim_check()
sim_check_wo_stop_word()
syn_sim_check()
morph_sim_check()
ngram_sim_check()
frame_check()