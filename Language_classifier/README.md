# Documentation for the Document Classification Language Code

This document describes the operation and components of the language module. This module classifies markdown documents based on the percentage of languages detected. The process is divided into two main models: a classification model that works as a filter and a classification model for the rest of the documents.


## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#pre-requirements-prerequisites)
3. [Description of Functions](#description-of-functions)
4. [First Model: Filter](#first-filter-model)
Second Model: Classification](#second-model-classification) 6.
6. [Execution and Results](#execution-and-results)

## Introduction

The aim of this module is to classify documents according to the percentages of English and Spanish language membership. The first model acts as a filter to identify documents with high percentages of belonging to a specific language, while the second model classifies the remaining documents with lower percentages of belonging to a language.

## Prerequisites

Make sure you have the following packages installed:

- `re`
- `collections`
- `langdetect`
- `nltk`
- `spacy`

In addition, download the necessary ‘NLTK’ resources (‘punkt’, ‘stopwords’ and ‘wordnet’), and install and load the ‘spaCy’ templates (‘en_core_web_sm’ and ‘es_core_news_sm’) for English and Spanish:

## Functional Description

### `preprocessing_prev(text)`.

Removes nested code blocks, tables, braces and shell code comments from text.

### `preprocessing(text)`.

Removes various unwanted text structures, such as empty lines, parentheses, inverted commas, bold, italics, links and capitalised words.

### `clean_tokens(tokens)`.

Clean and filter tokens by removing stopwords and converting them to lowercase.

### `process_file_for_filter(file_path)`.

Processes a file to calculate language membership percentages using common words and lemmatisation. Performs preprocessing, digit stripping and removal of words starting with capital letters.

### `filter_files(directory_path)`.

Filter files by the smallest percentage of language membership, separating files with less than 5% and more than 5%.

### `is_english_word(word)`.

Checks if a word is English using ‘WordNet’.

### `is_spanish_word(word)`.

Checks if a word is Spanish using ‘WordNet’.

### `classify_words(tokens)`.

Classify tokens into English or Spanish words, using `WordNet` and `langdetect` for ambiguous cases.

### `process_file_main(file_path)`.

Processes a file and calculates the percentages of English and Spanish membership, using the `classify_words` function and `spaCy` lemmatisation.

### `process_multiple_files(filtered_files)`.

Processes multiple files and counts how many meet different membership percentage conditions.

## First Model: Filter

The first model is used to filter documents that have high percentages of belonging to a specific language.

1. **Preprocessing**: Code blocks, tables and a little basic preprocessing such as removal of digits and capitalised words are removed.
2. **Tokenisation and Filtering**: Text is tokenised and stopwords are removed.
3. **Language Classification**: Percentages of belonging to each language are calculated using common words and lemmatisation.
4. **File Filtering**: Files are filtered into two categories: those with membership percentages lower and higher than 5%.

## Second Model: Classification

The second model is applied to the remaining documents with lower language membership percentages greater than 5%.

1. **Preprocessing**: The first model's preprocessing is supplemented by the removal of unwanted text structures.
2. **Tokenisation and Filtering**: The text is tokenised and more complex stopwords and matching words are removed.
3. **Word Classification**: Words are classified into English or Spanish words using ‘WordNet’ and ‘langdetect’.
4. **Percentage Calculation**: Percentages of English and Spanish membership are calculated using `spaCy` lemmatisation.
5. 5. **Classification Conditions**: Documents that meet different percentage membership conditions (less than 25%, between 25% and 40%, and between 40% and 50%) are counted.

## Execution and Results

The code is executed by specifying the path to the directory with the markdown files. Then, the files are filtered and sorted according to the percentages of English and Spanish membership. Finally, the results and the paths of the files that meet certain conditions are printed.

## Additional information

All this documentation provides a structured and automated way of classifying documents according to language membership rates, using advanced natural language processing and lemmatisation techniques.