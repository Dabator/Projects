# Language Classification of Words in a Text (NLP)

## Overview

This project demonstrates a method to classify words/tokens in a given text according to their language (Spanish or English). The process includes preprocessing the text, removing stopwords, classifying words, and calculating the percentage of words belonging to each language. Additionally, it includes extracting named entities, specifically person names, from the text.

## Requirements

- Python 3.x 
- Libraries: `nltk`, `spacy`, `sklearn`, `langdetect`
- Download necessary NLTK resources:

    ```python
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    ```

- Download the spaCy language models:

    ```sh
    python -m spacy download en_core_web_sm
    python -m spacy download es_core_news_sm
    ```

## Preprocessing

### Text Cleaning

- Remove words that are completely in uppercase.
- Remove digits from the text.

### Tokenization

- Tokenize the cleaned text using NLTK.

### Named Entity Extraction

- Extract person entities using NLTK's named entity recognition (NER) and remove them from the list of tokens.

## Stopword Removal

- Remove stopwords for both English and Spanish using NLTK's stopwords list.

## Word Classification

- **Check Language Using WordNet**:

    - Define functions to check if a word exists in English or Spanish using WordNet.
    - Use additional dictionaries for common words not recognized by WordNet.

- **Language Detection**:

    - If a word could belong to both languages, use the `langdetect` library to determine the language.

## Lemmatization

- Lemmatize words using spaCy after they have been classified into English or Spanish.

## Output

- Print lists of lemmatized English and Spanish words.
- Calculate and print the percentage of words in each language.

## How to Run

1. Ensure you have Python 3.x installed.
2. Install the required libraries using:

    ```sh
    pip install nltk spacy scikit-learn langdetect
    ```

3. Download the necessary NLTK data:

    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    ```

4. Download the spaCy language models:

    ```sh
    python -m spacy download en_core_web_sm
    python -m spacy download es_core_news_sm
    ```

5. Replace `contenido_md` with your input text.

