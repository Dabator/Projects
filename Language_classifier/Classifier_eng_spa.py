import re
import nltk
import spacy
from nltk.corpus import stopwords, wordnet
from nltk import ne_chunk, pos_tag
from sklearn.feature_extraction.text import CountVectorizer
from langdetect import detect_langs

# Download necessary resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load spaCy models for English and Spanish
nlp_en = spacy.load("en_core_web_sm")
nlp_es = spacy.load("es_core_news_sm")

with open('README_AC.md', 'r') as file:
    contenido_md = file.read()


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


# Preprocesamiento básico
def preprocesing(text):
    # Eliminar palabras que estén completamente en mayúsculas
    text = ' '.join(word for word in text.split() if not word.isupper())
    # Eliminar dígitos
    text = re.sub(r'\d+', '', text)
    # Tokenizar el texto
    text = nltk.word_tokenize(text)
    # EXTRACCION ENTITIES 
    text = extract_person_entities(text)

    return text

tokens = preprocesing(contenido_md)

# Lista de idiomas y sus códigos para stopwords
stopwords_lang = {
    "spanish": set(stopwords.words("spanish")),
    "english": set(stopwords.words("english")),
    "comun": {"actual", "central", "normal", "base", "final", "local", "son", "simple",
              "popular", "radio", "total", "color", "describe", "sin", "sea", "use", "oral",
              "error", "familiar", "global", "informal", "original", "social", "super", "universal",
              "capital", "continental", "comun", "festival", "final", "ideal", "legal", "natural",
              "personal", "real", "tradicional", "virtual", "digital", "material", "mental",
              "social", "visual", "editor", "horizontal", "vertical"}
}

# Eliminar stopwords para cada idioma
tokens = [token.lower() for token in tokens if token.isalnum()]
tokens = [token for token in tokens if token not in stopwords_lang["spanish"] and 
          token not in stopwords_lang["english"] and token not in stopwords_lang["comun"]]

# Funciones de idioma usando WordNet
def is_english_word(word):
    synsets = wordnet.synsets(word)
    return len(synsets) > 0

def is_spanish_word(word):
    synsets = wordnet.synsets(word, lang='spa')
    return bool(synsets)


# Calcular probabilidades de pertenencia a cada idioma y clasificar palabras
def classify_words(tokens):
    english_words = set()
    spanish_words = set()

    for token in tokens:
        english = is_english_word(token)
        spanish = is_spanish_word(token)

        if english and not spanish:
            english_words.add(token)
        elif spanish and not english:
            spanish_words.add(token)
        else:
            # Si la palabra es ambigua, utiliza langdetect
            try:
                detected_langs = detect_langs(token)
                detected_lang = max(detected_langs, key=lambda x: x.prob).lang
                if detected_lang == 'en':
                    english_words.add(token)
                else: spanish_words.add(token)
            
            except:
                continue

    return english_words, spanish_words

# Clasificar palabras
english_words, spanish_words = classify_words(tokens)

# Lematizar palabras clasificadas por idioma
english_lemmatized = list(set([nlp_en(word)[0].lemma_ for word in english_words]))
spanish_lemmatized = list(set([nlp_es(word)[0].lemma_ for word in spanish_words]))

# Mostrar los resultados
print("English Words:", english_lemmatized)
print("Spanish Words:", spanish_lemmatized)

# Calcular y mostrar los porcentajes
total_words = len(english_lemmatized) + len(spanish_lemmatized)
english_percentage = (len(english_lemmatized) / total_words) * 100 if total_words > 0 else 0
spanish_percentage = (len(spanish_lemmatized) / total_words) * 100 if total_words > 0 else 0

print(f"English: {english_percentage:.2f}%")
print(f"Spanish: {spanish_percentage:.2f}%")
