# Documentación para la Clasificación de Documentos por Idioma

Este documento explica cómo funciona un módulo que clasifica documentos en función del idioma en el que están escritos. El sistema trabaja con documentos en formato 'markdown' y puede identificar si están en inglés o español. La clasificación se realiza en dos etapas principales.

## Tabla de Contenidos

- [Documentación para la Clasificación de Documentos por Idioma](#documentación-para-la-clasificación-de-documentos-por-idioma)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Introducción](#introducción)
  - [Requisitos Previos](#requisitos-previos)
  - [Descripción del Proceso](#descripción-del-proceso)
    - [Preprocesamiento de Documentos](#preprocesamiento-de-documentos)
    - [Análisis de Texto](#análisis-de-texto)
    - [Clasificación por Idioma](#clasificación-por-idioma)
    - [Filtrado de Documentos](#filtrado-de-documentos)
    - [Clasificación Detallada](#clasificación-detallada)
  - [Primer Modelo: Filtro](#primer-modelo-filtro)
  - [Segundo Modelo: Clasificación](#segundo-modelo-clasificación)
  - [Ejecución y Resultados](#ejecución-y-resultados)

## Introducción

El objetivo de este sistema es clasificar documentos según si están escritos en inglés o español. La primera etapa identifica rápidamente documentos que están claramente en un solo idioma, mientras que la segunda etapa clasifica documentos que no están tan claros.

## Requisitos Previos

Para usar este sistema, asegúrese de tener instalado el software necesario y seguir los pasos de instalación recomendados.

## Descripción del Proceso

### Preprocesamiento de Documentos

Primero, el sistema limpia el texto del documento para eliminar elementos no deseados, como fragmentos de código, tablas y comentarios. Esto ayuda a centrarse solo en el contenido relevante.

### Análisis de Texto

Luego, el sistema examina el texto del documento y lo organiza en partes manejables. Se eliminan palabras que no son importantes para la clasificación, como nombres de sitios web o números.

### Clasificación por Idioma

El sistema analiza el texto para determinar si las palabras usadas son más comunes en inglés o en español. Usa una serie de técnicas para contar cuántas palabras en cada idioma hay en el documento.

### Filtrado de Documentos

Los documentos se dividen en dos grupos: aquellos en los que un idioma es claramente predominante (menos del 5%) y aquellos donde el idioma predominante no es tan claro (más del 5%).

### Clasificación Detallada

Para los documentos que no están claros, el sistema realiza un análisis más detallado. Clasifica las palabras en inglés o español y calcula qué porcentaje del documento está en cada idioma.

## Primer Modelo: Filtro

En esta etapa, el sistema identifica documentos que están claramente en un solo idioma.

1. **Limpieza Inicial**: Se eliminan elementos no relevantes del texto, como bloques de código y tablas.
2. **Organización del Texto**: Se prepara el texto para el análisis eliminando palabras y números innecesarios.
3. **Cálculo de Porcentajes**: Se determina el porcentaje de texto en cada idioma.
4. **Clasificación de Documentos**: Los documentos se dividen en aquellos donde un idioma es claramente predominante (más del 5%) y aquellos donde el idioma predominante no es tan claro (menos del 5%).

## Segundo Modelo: Clasificación

Para los documentos que no están claramente en un solo idioma, el sistema realiza un análisis más detallado.

1. **Limpieza Adicional**: Se realiza una limpieza más exhaustiva para eliminar cualquier contenido no deseado.
2. **Análisis Detallado**: Se organizan y filtran las palabras para mejorar la precisión de la clasificación.
3. **Clasificación de Palabras**: Se identifican las palabras en inglés o español.
4. **Cálculo de Porcentajes Detallados**: Se calculan los porcentajes de texto en cada idioma con mayor precisión.
5. **Resultados de Clasificación**: Se cuentan los documentos que cumplen con diferentes condiciones de porcentaje de texto en cada idioma.

## Ejecución y Resultados

Para usar el sistema, especifique la carpeta donde se encuentran los documentos. El sistema filtrará y clasificará los documentos según el porcentaje de texto en cada idioma. Luego, se mostrarán los resultados y las rutas de los documentos que cumplen con las condiciones establecidas.

Esta documentación proporciona una explicación sencilla de cómo el sistema clasifica documentos según el idioma en el que están escritos, utilizando un proceso estructurado y automatizado.
