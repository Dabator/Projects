# Language Classification of Words in a Text (PLN)

## Overview

This project demonstrates a method to classify words/tokens in a given text according to their language (Spanish or English). The process includes preprocessing the text, removing stopwords, classifying words, and calculating the percentage of words belonging to each language. Additionally, it includes extracting named entities, specifically person names, from the text.

## Requirements
- Python 3.x 
- Libraries: nltk, spacy, sklearn 
- Download necessary NLTK resources:

    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

- Download the spaCy language models:

    python -m spacy download en_core_web_sm
    python -m spacy download es_core_news_sm

## Preprocessing

### Text Cleaning:

- Remove words that are completely in uppercase. 
- Remove digits from the text. 

### Tokenization:

- Tokenize the cleaned text using NLTK.

### Named Entity Extraction:

- Extract person entities using NLTK's named entity recognition (NER) and remove them from the list of tokens. 

## Stopword Removal

- Remove stopwords for both English and Spanish using NLTK's stopwords list. 

## Word Classification

- Check Language Using WordNet:

    - Define functions to check if a word exists in English or Spanish using WordNet.

    - Use additional dictionaries for common words not recognized by WordNet.

- Context Analysis for Ambiguous Words:

    - If a word could belong to both languages, analyze its context using N-grams to determine the probability of belonging to each language.

## Lemmatization

- Lemmatize words using spaCy after they have been classified into English or Spanish.

## Output

- Print lists of lemmatized English and Spanish words. 
- Calculate and print the percentage of words in each language. 


# How to Run

- Ensure you have Python 3.x installed. 
- Install the required libraries using:

(sh)
pip install nltk spacy scikit-learn

- Download the necessary NLTK data:

(python)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

- Download the spaCy language models: 

(sh)
python -m spacy download en_core_web_sm
python -m spacy download es_core_news_sm

- Replace contenido_md with your input text.

- Run the script to see the classified words and their respective percentages.

This script offers a comprehensive approach to language classification of words in a bilingual text, using a combination of tokenization, stopword removal, context analysis with N-grams, and lemmatization.


