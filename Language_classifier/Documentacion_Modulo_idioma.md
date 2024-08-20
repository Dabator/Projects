# Documentación para el Código de Clasificación de Documentos por Idioma

Este documento describe el funcionamiento y los componentes del módulo de idioma. Este módulo clasifica documentos 'markdown' en función de los porcentajes de idiomas detectados. El proceso se divide en dos modelos principales: un modelo de clasificación que funciona como filtro y un modelo de clasificación para el resto de los documentos.


## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Descripción de Funciones](#descripción-de-funciones)
4. [Primer Modelo: Filtro](#primer-modelo-filtro)
5. [Segundo Modelo: Clasificación](#segundo-modelo-clasificación)
6. [Ejecución y Resultados](#ejecución-y-resultados)

## Introducción

El objetivo de este módulo es clasificar documentos en función de los porcentajes de pertenencia a los idiomas inglés y español. El primer modelo actúa como un filtro para identificar documentos con altos porcentajes de pertenencia a un idioma específico, mientras que el segundo modelo clasifica los documentos restantes con menores porcentajes de pertenencia a un idioma.

## Requisitos Previos

Asegúrese de tener instalados los siguientes paquetes:

- `re`
- `collections`
- `langdetect`
- `nltk`
- `spacy`

Además, descargue los recursos necesarios de 'NLTK' ('punkt', 'stopwords' y 'wordnet'), e instale y cargue los modelos de 'spaCy' ("en_core_web_sm" y "es_core_news_sm") para inglés y español:

## Descripción de Funciones

### `preprocesing_prev(text)`

Elimina bloques de código anidados, tablas, códigos entre llaves y comentarios de código 'shell' del texto.

### `preprocesing(text)`

Elimina varias estructuras de texto no deseadas, como líneas vacías, paréntesis, comillas, negritas, cursivas, enlaces y palabras en mayúsculas.

### `clean_tokens(tokens)`

Limpia y filtra los tokens eliminando 'stopwords' y convirtiéndolos a minúsculas.

### `process_file_for_filter(file_path)`

Procesa un archivo para calcular los porcentajes de pertenencia a cada idioma utilizando palabras comunes y lematización. Realiza preprocesado, eliminación de dígitos y eliminación de palabras que comienzan en mayúsculas.

### `filter_files(directory_path)`

Filtra archivos según el porcentaje menor de pertenencia a un idioma, separando archivos con menos del 5% y más del 5%.

### `is_english_word(word)`

Verifica si una palabra es inglesa utilizando 'WordNet'.

### `is_spanish_word(word)`

Verifica si una palabra es española utilizando 'WordNet'.

### `classify_words(tokens)`

Clasifica los tokens en palabras inglesas o españolas, utilizando 'WordNet' y 'langdetect' para casos ambiguos.

### `process_file_main(file_path)`

Procesa un archivo y calcula los porcentajes de pertenencia a inglés y español, utilizando la función `classify_words` y la lematización de `spaCy`.

### `process_multiple_files(filtered_files)`

Procesa múltiples archivos y cuenta cuántos cumplen con diferentes condiciones de porcentajes de pertenencia.

## Primer Modelo: Filtro

El primer modelo se utiliza para filtrar documentos que tienen altos porcentajes de pertenencia a un idioma específico.

1. **Preprocesamiento**: Se eliminan bloques de código, tablas y un pequeño preprocesamiento básico como eliminación de dígitos y palabras en mayúscula.
2. **Tokenización y Filtrado**: Se tokeniza el texto y se eliminan stopwords.
3. **Clasificación de Idiomas**: Se calculan los porcentajes de pertenencia a cada idioma utilizando palabras comunes y lematización.
4. **Filtrado de Archivos**: Se filtran los archivos en dos categorías: aquellos con porcentajes de pertenencia menores y mayores al 5%.

## Segundo Modelo: Clasificación

El segundo modelo se aplica a los documentos restantes con porcentajes de pertenencia del idioma, de menor proporción, mayores al 5%.

1. **Preprocesamiento**: Se suma al preprocesamiento del primer modelo la eliminación de estructuras de texto no deseadas.
2. **Tokenización y Filtrado**: Se tokeniza el texto y se eliminan stopwords más complejas, así como palabras coincidentes.
3. **Clasificación de Palabras**: Se clasifican las palabras en inglesas o españolas utilizando 'WordNet' y 'langdetect'.
4. **Cálculo de Porcentajes**: Se calculan los porcentajes de pertenencia a inglés y español utilizando lematización de `spaCy`.
5. **Condiciones de Clasificación**: Se cuentan los documentos que cumplen con diferentes condiciones de porcentajes de pertenencia (menores de 25%, entre 25% y 40%, y entre 40% y 50%).

## Ejecución y Resultados

El código se ejecuta especificando la ruta del directorio con los archivos markdown. Luego, se filtran y clasifican los archivos según los porcentajes de pertenencia a inglés y español. Finalmente, se imprimen los resultados y las rutas de los archivos que cumplen con ciertas condiciones.

## Información adicional

Toda esta documentación proporciona una forma estructurada y automatizada de clasificar documentos en función de los porcentajes de pertenencia a diferentes idiomas, utilizando técnicas avanzadas de procesamiento de lenguaje natural y lematización.