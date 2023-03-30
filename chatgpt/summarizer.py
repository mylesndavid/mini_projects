# Import the necessary libraries
import requests
import string
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

# Define a function to clean and preprocess the text
def preprocess_text(text):
    # Remove punctuation and special characters
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Convert the text to lowercase
    text = text.lower()

    # Split the text into individual words
    words = text.split()

    # Remove stopwords
    stop_words = stopwords.words('english')
    words = [w for w in words if w not in stop_words]

    # Return the cleaned and preprocessed text
    return " ".join(words)

# Define a function to summarize the text
def summarize_text(text, ratio=0.1):
    # Preprocess the text
    text = preprocess_text(text)
    text_tokens = text.split()

    # Split the text into sentences
    sentences = text.split(".")

    # Create a matrix of sentence vectors
    sentence_vectors = []
    for sentence in sentences:
        sentence_tokens = sentence.split()
        sentence_vector = np.zeros(len(text.split()))
        for token in sentence_tokens:
            if token in text_tokens:
                sentence_vector[text_tokens.index(token)] += 1
        sentence_vectors.append(sentence_vector)

    # Create a similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                similarity_matrix[i][j] = cosine_distance(sentence_vectors[i], sentence_vectors[j])

    # Create a graph from the similarity matrix
    similarity_graph = nx.from_numpy_array(similarity_matrix)

    # Extract the sentences with the highest scores as the summary
    scores = nx.pagerank(similarity_graph)
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    number_of_sentences = int(len(ranked_sentences) * ratio)
    summary = []
    for i in range(number_of_sentences):
        summary.append(ranked_sentences[i][1])

    # Return the summary as a single string
    return ". ".join(summary)

# Define the main function
def main():
    # Prompt the user for the URL or filename of the webpage or document
    url_or_filename = input("Enter the URL or filename of the webpage or document: ")

    # Check if the input is a URL or a filename
    if url_or_filename.startswith("http"):
        # If it's a URL, download the webpage
        response = requests.get(url_or_filename)
        text = response.text
    else:
        # If it's a filename, read the file
        with open(url_or_filename, "r") as f:
            text = f.read()

    # Summarize the text
    summary = summarize_text(text)

    # Print the summary
    print(summary)

# Call the main function
if __name__ == "__main__":
    main()
