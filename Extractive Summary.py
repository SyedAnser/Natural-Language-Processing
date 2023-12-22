import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

def read_text(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

def sentence_similarity(sent1, sent2, stopwords):
    words1 = [word.lower() for word in sent1 if word not in stopwords]
    words2 = [word.lower() for word in sent2 if word not in stopwords]
    
    # Create a set of unique words in both sentences
    all_words = list(set(words1 + words2))
    
    # Initialize vectors with zeros
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
    
    # Populate the vectors with word frequencies
    for word in words1:
        vector1[all_words.index(word)] += 1
    
    for word in words2:
        vector2[all_words.index(word)] += 1
    
    # Calculate cosine similarity
    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stopwords):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i == j:
                continue
            similarity_matrix[i][j] = sentence_similarity(sentences[i], sentences[j], stopwords)
    
    return similarity_matrix

def generate_summary(file_path, num_sentences=5):
    text = read_text(file_path)
    sentences = sent_tokenize(text)
    stopwords_list = set(stopwords.words('english'))
    
    # Create a similarity matrix
    similarity_matrix = build_similarity_matrix(sentences, stopwords_list)
    
    # Convert the similarity matrix into a graph
    graph = nx.from_numpy_array(similarity_matrix)
    
    # Use the PageRank algorithm to rank sentences
    scores = nx.pagerank(graph)
    
    # Sort the sentences by their score in descending order
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    
    # Extract the top 'num_sentences' sentences to create the summary
    summary = [sentence for score, sentence in ranked_sentences[:num_sentences]]
    
    return ' '.join(summary)


input_file = "C:/Users/syeda/OneDrive/Desktop/codes/NLP/txt2.txt"
summary = generate_summary(input_file, num_sentences=10)  # Adjust the number of sentences as needed
print(summary)
