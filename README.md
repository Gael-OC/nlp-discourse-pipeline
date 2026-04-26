# Análisis de Discursos Políticos con NLP

Pipeline de extracción, procesamiento y análisis no supervisado de discursos políticos en español. El sistema consolida intervenciones desde redes sociales (X/Twitter) y medios de comunicación chilenos (Cooperativa, La Tercera), aplicando técnicas de vectorización, clustering y reducción dimensional para identificar patrones temáticos, alianzas discursivas y líneas ideológicas implícitas en el corpus.

---

## Tabla de Contenidos

- [Descripción](#descripción)
- [Arquitectura del Pipeline](#arquitectura-del-pipeline)
- [Requisitos](#requisitos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Configuración](#configuración)
- [Uso](#uso)
- [Resultados y Visualizaciones](#resultados-y-visualizaciones)
- [Notas Técnicas](#notas-técnicas)
- [Autores](#autores)

---

## Descripción

Este proyecto implementa un pipeline completo de análisis de discursos políticos que permite:

- **Recopilar** intervenciones políticas desde múltiples fuentes digitales en tiempo real.
- **Preprocesar** textos en español eliminando ruido semántico (HTML, URLs, menciones, hashtags, stopwords).
- **Vectorizar** el corpus mediante TF-IDF con selección de características por varianza.
- **Agrupar** discursos similares mediante K-Means no supervisado.
- **Visualizar** la estructura del discurso político mediante reducción dimensional comparativa (PCA, t-SNE, UMAP).
- **Identificar** términos distintivos por cluster para caracterizar líneas discursivas.
- **Persistir** resultados tanto en archivos Parquet locales como en MongoDB.

El enfoque permite detectar convergencias y divergencias temáticas entre fuentes informativas tradicionales y conversación digital en redes sociales.

---

## Arquitectura del Pipeline

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Fuentes      │     │  Cache Local    │     │ Preprocesamiento│
│ X / Cooperativa │────▶│  Raw Parquet    │────▶│   (limpieza)    │
│  / La Tercera   │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
┌─────────────────┐     ┌─────────────────┐     ┌────────▼────────┐
│    MongoDB      │◀────│  Final Parquet  │◀────│  Ingeniería de  │
│   (cloud/DB)    │     │  (clusterizado) │     │  Características│
└─────────────────┘     └─────────────────┘     │  TF-IDF + K-Means│
                                                └────────┬────────┘
                                                         │
                                                ┌────────▼────────┐
                                                │  Visualización  │
                                                │ Matplotlib + WC │
                                                └─────────────────┘
```

### Etapas del flujo

1. **Adquisición**: extracción desde API de X y feeds RSS.
2. **Normalización**: consolidación de esquemas y persistencia cruda.
3. **Preprocesamiento**: limpieza lingüística y filtrado de stopwords en español.
4. **Análisis Vectorial**: TF-IDF, selección de características y clustering K-Means.
5. **Reducción Dimensional**: PCA (lineal global), t-SNE (local) y UMAP (híbrido).
6. **Visualización**: frecuencias, dispersión por fuente, comparativa de métodos y nubes de palabras.
7. **Persistencia**: almacenamiento en Parquet y MongoDB con clave única compuesta.

---

## Requisitos

- Python 3.10
- Cuenta de desarrollador en X con acceso al endpoint `search/recent`
- Instancia de MongoDB (local o Atlas)

### Entorno Conda

El proyecto utiliza un entorno Conda con las siguientes dependencias principales:

```yaml
name: ml_lab1
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10.20
  - pandas=2.3.3
  - numpy=2.2.5
  - scikit-learn=1.7.2
  - matplotlib=3.10.8
  - nltk=3.9.4
  - umap-learn=0.5.11
  - pymongo=4.15.5
  - feedparser=6.0.12
  - requests=2.33.1
  - pyarrow=23.0.1
  - fastparquet=2025.12.0
  - pillow=12.1.1
  - numba=0.65.0
  - pynndescent=0.6.0
  - wordcloud          # pip install wordcloud
```

> El archivo `environment.yml` completo con todas las dependencias resueltas está disponible en el repositorio.

### Instalación rápida

```bash
conda env create -f environment.yml
conda activate ml_lab1
```

---

## Estructura del Proyecto

```
.
├── config.py                 # Credenciales y parámetros de configuración
├── main.py                   # Orquestador principal del pipeline
├── fuentes.py                # Módulo de extracción (X API + RSS)
├── preprocessing.py          # Limpieza de texto y normalización lingüística
├── features.py               # Vectorización TF-IDF, clustering y reducción dimensional
├── visualization.py          # Gráficos de frecuencias y PCA por fuente
├── visualization_1_2.py      # Comparativa PCA/t-SNE/UMAP y nubes de palabras
├── database.py               # Capa de persistencia en MongoDB
├── environment.yml           # Definición completa del entorno Conda
├── data/
│   ├── raw/
│   │   └── corpus_crudo.parquet
│   └── processed/
│       ├── corpus_limpio.parquet
│       └── corpus_final_clusterizado.parquet
└── README.md
```

---

## Configuración

Todas las variables sensibles y parámetros de búsqueda se centralizan en `config.py`.

| Variable | Descripción |
|----------|-------------|
| `X_BEARER_TOKEN` | Bearer Token de la API de X (solicitado vía `getpass`) |
| `MONGODB_URI` | URI de conexión a MongoDB (solicitado vía `getpass`) |
| `X_QUERY` | Query de búsqueda para captura de discursos políticos |
| `X_MAX_RESULTS` | Límite de posts a descargar (default: 500) |
| `COOPERATIVA_RSS_URL` | Feed RSS del medio Cooperativa |
| `LATERCERA_RSS_URL` | Feed RSS del medio La Tercera |
| `MONGO_DB_NAME` | Nombre de la base de datos en MongoDB |
| `MONGO_COLLECTION_NAME` | Nombre de la colección de documentos |

> **Seguridad**: las credenciales se solicitan de forma interactiva mediante `getpass()` para evitar su exposición en el código fuente o en repositorios.

---

## Uso

### Ejecución completa del pipeline

```bash
conda activate ml_lab1
python main.py
```

El orquestador detecta automáticamente la existencia de un corpus crudo local:
- **Si existe cache**: omite la extracción y reutiliza los datos crudos.
- **Si no existe cache**: realiza la extracción completa, guarda en `data/raw/` y continúa el procesamiento.

### Flujo detallado

1. **Extracción**: descarga posts de X y noticias de RSS según los parámetros configurados.
2. **Consolidación**: normaliza metadatos y une todas las fuentes en un único DataFrame.
3. **Preprocesamiento**: aplica limpieza profunda generando la columna `texto_limpio`.
4. **Vectorización**: construye matriz TF-IDF (máx. 1000 features) y selecciona características por varianza.
5. **Clustering**: ejecuta K-Means con `k=4` (ajustable dinámicamente según tamaño del corpus).
6. **Reducción dimensional**: computa embeddings 2D mediante PCA, t-SNE y UMAP.
7. **Visualización**: genera gráficos exploratorios y nubes de palabras por cluster.
8. **Persistencia**: guarda datasets intermedios en Parquet y documentos finales en MongoDB.

---

## Resultados y Visualizaciones

### 1. Top 20 términos más frecuentes
Gráfico de barras con los términos dominantes del corpus post-limpieza, permitiendo identificar ejes temáticos centrales del discurso político capturado.

### 2. Dispersión PCA por fuente
Scatter plot en 2D coloreado por origen (X, Cooperativa, La Tercera) que revela la proximidad o divergencia discursiva entre medios tradicionales y conversación digital.

### 3. Comparativa de estrategias de reducción dimensional
Panel de tres gráficos que contrasta:
- **PCA**: preserva estructura global lineal.
- **t-SNE**: enfatiza vecindarios locales (perplexity adaptativo).
- **UMAP**: equilibra estructura local y global en el espacio vectorial.

### 4. Nubes de palabras por cluster
Para cada cluster K-Means, se genera una nube de palabras con los términos más representativos, facilitando la interpretación semántica de cada agrupación discursiva.

---

## Notas Técnicas

- **Anti-duplicados**: cada documento en MongoDB utiliza una clave compuesta `_id = fuente::id` con operación `upsert`, garantizando idempotencia en recargas.
- **Reproducibilidad**: todas las operaciones estocásticas (K-Means, PCA, t-SNE, UMAP) fijan `random_state=42`.
- **Robustez**: el pipeline maneja corpus de tamaño variable. Los parámetros de `perplexity` (t-SNE) y `n_neighbors` (UMAP) se ajustan dinámicamente si el dataset es pequeño, evitando errores de ejecución.
- **Idioma**: el preprocesamiento está optimizado para español mediante stopwords de NLTK y normalización de caracteres especiales (tildes, eñes).
- **Persistencia dual**: el uso de Parquet permite análisis offline y reproducibilidad local; MongoDB habilita consultas distribuidas y escalabilidad.

---

## Autores

- **Gael Ortega** - *Estudiante de Ingeniería en Tecnologías de Información* - Universidad Católica del Norte.
- **Matías Vidal** - *Estudiante de Ingeniería en Tecnologías de Información* - Universidad Católica del Norte.

---
