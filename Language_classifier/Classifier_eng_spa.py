import re
import nltk
import spacy
from markdown import markdown
from nltk.corpus import stopwords, wordnet
from sklearn.feature_extraction.text import CountVectorizer

# Download necessary resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load spaCy models for English and Spanish
nlp_en = spacy.load("en_core_web_sm")
nlp_es = spacy.load("es_core_news_sm")

with open('README_AC.md', 'r') as file:
    contenido_md = file.read()

# Example text
text = contenido_md

# Remove words that are completely uppercase
text = ' '.join(word for word in text.split() if not word.isupper())

# Remove digits
text = re.sub(r'\d+', '', text)

# Tokenize the text
tokens = nltk.word_tokenize(text)

# ENTITY EXTRACTION
def extract_person_entities(tokens):
    tagged_tokens = nltk.pos_tag(tokens)
    tree = nltk.ne_chunk(tagged_tokens)
    
    person_entities = []
    for subtree in tree:
        if isinstance(subtree, nltk.Tree) and subtree.label() == 'PERSON':
            entity = " ".join([token for token, pos in subtree.leaves()])
            person_entities.append(entity)

    non_person_tokens = [token for token, pos in tagged_tokens if token not in person_entities]

    return non_person_tokens

tokens = extract_person_entities(tokens)

# List of languages and their codes for stopwords
stopwords_lang = {
    "spanish": set(stopwords.words("spanish")),
    "english": set(stopwords.words("english"))
}

# Remove stopwords for each language
tokens = [token.lower() for token in tokens if token.isalnum()]
tokens = [token for token in tokens if token not in stopwords_lang["spanish"] and token not in stopwords_lang["english"]]

# Language functions using WordNet
def is_english_word(word):
    synsets = wordnet.synsets(word)
    return len(synsets) > 0

def is_spanish_word(word):
    synsets = wordnet.synsets(word, lang='spa')
    return bool(synsets)

# Additional dictionary of common English and Spanish words not recognized by WordNet
additional_english_words = set(['other', 'roadmaps', 'objetive', 'without','recomended', 'test'])
additional_spanish_words = set(["facilitator", "si", "alto", "principal", "actual", "continuo", "favor", "idea", "junto", "toda"])

# Calculate language probabilities and classify words
def classify_words(tokens):
    english_words = set()
    spanish_words = set()

    for token in tokens:
        english = is_english_word(token) or token in additional_english_words
        spanish = is_spanish_word(token) or token in additional_spanish_words

        if english and not spanish:
            english_words.add(token)
        elif spanish and not english:
            spanish_words.add(token)
        else:
            # If the word is ambiguous, analyze the context using N-Grams
            context = get_context(tokens, token)
            if context:
                english_prob = calculate_ngram_probability(context, 'english')
                spanish_prob = calculate_ngram_probability(context, 'spanish')
                if english_prob > spanish_prob:
                    english_words.add(token)
                else:
                    spanish_words.add(token)

    return english_words, spanish_words

def get_context(tokens, target, window_size=2):
    index = tokens.index(target)
    start = max(index - window_size, 0)
    end = min(index + window_size + 1, len(tokens))
    context = tokens[start:end]
    return context

def calculate_ngram_probability(context, language):
    context_text = ' '.join(context)
    vectorizer = CountVectorizer(ngram_range=(1, 2), vocabulary=stopwords_lang[language])
    ngram_counts = vectorizer.fit_transform([context_text]).toarray()
    return ngram_counts.sum()

# Classify words
english_words, spanish_words = classify_words(tokens)

# Lemmatize classified words by language
english_lemmatized = [nlp_en(word)[0].lemma_ for word in english_words]
spanish_lemmatized = [nlp_es(word)[0].lemma_ for word in spanish_words]

# Calculate and display percentages
total_words = len(english_lemmatized) + len(spanish_lemmatized)
english_percentage = (len(english_lemmatized) / total_words) * 100 if total_words > 0 else 0
spanish_percentage = (len(spanish_lemmatized) / total_words) * 100 if total_words > 0 else 0

print(f"English: {english_percentage:.2f}%")
print(f"Spanish: {spanish_percentage:.2f}%")

# Display results
print("English Words:", english_lemmatized)
print("Spanish Words:", spanish_lemmatized)

