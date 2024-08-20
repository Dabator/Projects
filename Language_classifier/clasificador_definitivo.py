import re
from collections import Counter
from langdetect import DetectorFactory
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, download
from nltk.tokenize import word_tokenize
import string
import os
import nltk
import spacy
from nltk.corpus import wordnet
from langdetect import detect_langs

# Semilla para asegurar reproducibilidad
DetectorFactory.seed = 0

# Descargar recursos necesarios (si no están ya descargados)
#download('punkt')
#download('stopwords')
#download('wordnet')

# Cargar modelos de spaCy para inglés y español
nlp_en = spacy.load("en_core_web_sm")
nlp_es = spacy.load("es_core_news_sm")

# Lista de idiomas y sus códigos para stopwords más simples
common_words = {
    'en': ['the', 'and', 'to', 'of', 'in', 'that', 'it', 'is', 'was', 'I'],
    'es': ['el', 'y', 'de', 'a', 'en', 'que', 'la', 'es', 'y', 'yo'],
}

# Lista de idiomas y sus códigos para stopwords más completas y comunes en ambos idiomas
stopwords_lang = {
    "spanish": set(stopwords.words("spanish")),
    "english": set(stopwords.words("english")),
    "comun": {"actual", "central", "region", "normal", "base", "final", "local", "son", "simple",
              "popular", "radio", "total", "color", "describe", "sin", "sea", "use", "oral",
              "error", "familiar", "global", "informal", "original", "social", "super", "universal",
              "capital", "continental", "comun", "festival", "final", "ideal", "legal", "natural",
              "personal", "real", "tradicional", "virtual", "digital", "material", "mental",
              "social", "visual", "editor", "horizontal", "vertical", "idea"}
}

# Lematizador
lemmatizer = WordNetLemmatizer()

# Preprocesado avanzado de patrones
def preprocesing(text):
    # Eliminar líneas vacías resultantes
    texto_limpio = re.sub(r'\n\s*\n', '\n', text)
    # Definir los patrones específicos a eliminar
    patterns = [
        r'\([^)]*\)', # (texto)
        r'\"[^\"]*\"', # "texto"
        r'\*\*[^*]*\*\*',     # **texto**
        r'<[^>]*>',           # <texto>
        r'\'[^\']*\'',        # 'texto'
        r'\[[^\]]*\]',        # [texto]
        r'\{[^\}]*\}',        # {texto}
        r'\*[^\*]*\*',        # *texto*
        r'`[^`]*`',           # `texto`
        r'-"[^"]*"-',         # Frases entre -"texto"-
        r'_"[^"]*"_',         # Frases entre _"texto"_
        r'~~~[^~]*~~~',       # ~~~texto~~~
        r'https://[^\s]+',     # cualquier enlace que empiece por https
        r'http://[^\s]+',      # cualquier enlace que empiece por http
        r'\b[A-Z][a-zA-Z]*\b' # Palabras que comienzan con mayúscula
    ]
    # Unir todos los patrones en una sola expresión regular
    combined_pattern = '|'.join(patterns)
    # Eliminar todos los patrones del texto
    texto_limpio = re.sub(combined_pattern, '', texto_limpio, flags=re.DOTALL)
    # Eliminar dígitos
    texto_limpio = re.sub(r'\d+', '', texto_limpio)

    return texto_limpio

# Función para transformar tokens finales y eliminar las stopwords
def clean_tokens(tokens):
    # Convertir a minúsculas y eliminar carácteres especiales
    tokens = [token.lower() for token in tokens if token.isalnum()]
    # Eliminar stopwords y palabras comunes en inglés y español
    tokens = [token for token in tokens if token not in stopwords_lang["spanish"] and 
              token not in stopwords_lang["english"] and token not in stopwords_lang["comun"]]
    
    return tokens

# Eliminar bloques de código anidados, tablas, y código entre llaves
def preprocesing_prev(text):
    # Expresión regular para identificar y eliminar bloques de código que comienzan con ```shell y continúan hasta el siguiente bloque ```
    pattern = r'```Shell.*?```(?:\n|$)'
    # Eliminar los bloques de código y quedarse con el texto restante
    texto_limpio = re.sub(pattern, '', text, flags=re.DOTALL)
    # Expresión regular para identificar y eliminar bloques de texto que comienzan con { y continúan hasta el siguiente }
    pattern = r'\{.*?\}(?:\n|$)'
    # Eliminar los bloques de texto y quedarse con el texto restante
    texto_limpio = re.sub(pattern, '', texto_limpio, flags=re.DOTALL)
    # Expresión regular para identificar y eliminar tablas delimitadas por |
    pattern = r'(\|.*?\|(?:\n|$))+'
    texto_limpio = re.sub(pattern, '', texto_limpio, flags=re.DOTALL)
    # Adicionalmente eliminar cualquier línea que contenga URL o referencias a issues
    pattern_issue = r'- jira URL issue:.*'
    texto_limpio = re.sub(pattern_issue, '', texto_limpio)
    # También eliminar comentarios de código shell
    pattern_comment = r'#.*'
    texto_limpio = re.sub(pattern_comment, '', texto_limpio)
    # Expresión regular para identificar y eliminar los bloques de código en Markdown
    pattern = r'```(?:\w+\n)?(.*?)```'
    # Eliminar los bloques de código y quedarse con el texto restante
    texto_limpio = re.sub(pattern, '', texto_limpio, flags=re.DOTALL)
    # Expresión regular para identificar y eliminar bloques de código delimitados por llaves {}
    pattern = r'\{.*?\}'
    texto_limpio = re.sub(pattern, '', texto_limpio, flags=re.DOTALL)
    
    return texto_limpio


# PRIMER MODELO PARA FILTRADO

# Función para procesar individualmente cada documento
def process_file_for_filter(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    # Prepocesamiento
    content = preprocesing_prev(markdown_content)
    # Eliminar dígitos
    content = re.sub(r'\d+', '', content)
    # Eliminar palabras que comienzan en mayúscula
    content = re.sub(r'\b[A-Z][a-zA-Z]*\b', '', content)
    # Aplicar tabla de traducciones
    content = content.translate(str.maketrans('', '', string.punctuation))
    # Aplicar Segmentación de párrafos
    segments = content.split('\n')
    # Contabilización del lenguaje
    language_counts = Counter()
    # Uso de stops words para la traducción
    word_frequencies = {lang: Counter() for lang in common_words.keys()}
    unique_words_per_lang = {lang: set() for lang in common_words.keys()}
    
    for segment in segments:
        if segment.strip():
            words = word_tokenize(segment)
            words = [token.lower() for token in words if token.isalnum()]
            lang_scores = {lang: sum(word in words for word in common) for lang, common in common_words.items()}
            detected_lang = max(lang_scores, key=lang_scores.get)
            language_counts[detected_lang] += 1
            filtered_words = [word for word in words if word not in stopwords_lang.get(detected_lang, set())]
            
            tagged_tokens = pos_tag(filtered_words)
            lemmatized_words = {lemmatizer.lemmatize(word) for word, tag in tagged_tokens}
            
            unique_words_per_lang[detected_lang].update(lemmatized_words)
            word_frequencies[detected_lang].update(lemmatized_words)
    
    # Cálculo del porcentaje de idioma para un archivo
    total_unique_words = sum(len(words) for words in unique_words_per_lang.values())
    
    if total_unique_words > 0:
        language_percentages = {lang: (len(words) / total_unique_words) * 100 
                                for lang, words in unique_words_per_lang.items()}
    else:
        # Si la palabra no fue encontrada, se configura a 0
        language_percentages = {lang: 0 for lang in common_words.keys()}
    
    return language_percentages, word_frequencies

# Filtrado de archivos para todo el directorio
def filter_files(directory_path):
    less_than_5_files = []
    more_than_5_files = []
    
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith(".md"):
                file_path = os.path.join(root, filename)
                language_percentages, _ = process_file_for_filter(file_path)
                min_percentage = min(language_percentages.values())
                if min_percentage < 5:
                    less_than_5_files.append(file_path)
                else:
                    more_than_5_files.append(file_path)
    
    return less_than_5_files, more_than_5_files

#SEGUNDO MODELO

# Función para clasificación de idioma en inglés usando WordNet
def is_english_word(word):
    synsets = wordnet.synsets(word)
    return len(synsets) > 0

# Función para clasificación de idioma en inglés usando WordNet
def is_spanish_word(word):
    synsets = wordnet.synsets(word, lang='spa')
    return bool(synsets)

# Función para calcular probabilidades de pertenencia a cada idioma y clasificar palabras
def classify_words(tokens):
    # Iniciar contabilizador de palabras para inglés y español
    english_words = set()
    spanish_words = set()

    # Aplicación de Wordnet
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
                else:
                    spanish_words.add(token)
            except:
                continue

    return english_words, spanish_words

# Procesar un solo archivo y calcular los porcentajes
def process_file_main(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    # Preprocesado
    text = preprocesing_prev(text)
    text = preprocesing(text)
    tokens = nltk.word_tokenize(text)
    tokens = clean_tokens(tokens)
    # Uso de la función "classify_words" para clasificar cada documento
    english_words, spanish_words = classify_words(tokens)
    # Lematización
    english_lemmatized = [nlp_en(word)[0].lemma_ for word in english_words]
    spanish_lemmatized = [nlp_es(word)[0].lemma_ for word in spanish_words]
    # Calculo del porcentaje de cada idioma
    total_words = len(english_lemmatized) + len(spanish_lemmatized)
    english_percentage = (len(english_lemmatized) / total_words) * 100 if total_words > 0 else 0
    spanish_percentage = (len(spanish_lemmatized) / total_words) * 100 if total_words > 0 else 0

    return english_percentage, spanish_percentage

# Clasificación de archivos para el resto del directorio
def process_multiple_files(filtered_files):
    # Contabilizar archivos según porcentajes
    count25 = 0
    count25_40 = 0
    count40_50 = 0
    # Recopilación de rutas de los archivos clasificados
    files_matching_condition25_40 = []
    files_matching_condition40_50 = []
    # Uso de la función "process_file_main" para procesar cada documento y clasificarlo
    for file_path in filtered_files:
        english_percentage, spanish_percentage = process_file_main(file_path)
        # Verificar los porcentajes
        if min(english_percentage, spanish_percentage) >= 40:
            count40_50 += 1
            files_matching_condition40_50.append(file_path)
        elif min(english_percentage, spanish_percentage) <= 25:
            count25 += 1
        else:
            count25_40 += 1
            files_matching_condition25_40.append(file_path)

    return count25, count25_40, count40_50, files_matching_condition25_40, files_matching_condition40_50

# Ruta del directorio con los archivos markdown
directory_path = 'ruta_directorio_archivos' # Reemplaza con la ruta de tu directorio

# Filtrar los archivos según el porcentaje de idioma menor
less_than_5_files, more_than_5_files = filter_files(directory_path)

# Procesar los archivos que tienen el idioma de menor proporción superior al 5%
count25, count25_40, count40_50, files_matching_condition25_40, files_matching_condition40_50 = process_multiple_files(more_than_5_files)

# Mostrar el número de documentos clasificados para cada porcentaje
print(f"Número de documentos en los que el idioma de menor proporción es menor al 5%: {len(less_than_5_files)}")
print(f"Número de documentos en los que el idioma de menor proporción es menor al 25%: {count25}")
print(f"Número de documentos en los que el idioma de menor proporción es entre 25% y 40%: {count25_40}")
print(f"Número de documentos en los que el idioma de menor proporción es mayor al 40%: {count40_50}")

# Mostrar las rutas de los archivos que cumplen la condición
print("Archivos que cumplen la condición de 25 a 40:")
for file_path in files_matching_condition25_40:
    print(file_path)
print("Archivos que cumplen la condición de 40 a 50:")
for file_path in files_matching_condition40_50:
    print(file_path)
