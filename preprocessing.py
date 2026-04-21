import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

# Asegurar disponibilidad de stopwords localmente
try:
    STOPWORDS_ES = set(stopwords.words("spanish"))
except LookupError:
    nltk.download("stopwords", quiet=True)
    STOPWORDS_ES = set(stopwords.words("spanish"))

def limpiar_texto(texto):
    if not isinstance(texto, str):
        return ""
        
    texto = texto.lower()
    texto = re.sub(r"<[^>]+>", " ", texto)
    texto = re.sub(r"http\S+|www\.\S+", " ", texto)
    texto = re.sub(r"@\w+", " ", texto)
    texto = re.sub(r"[^a-záéíóúñü\s]", " ", texto)
    texto = re.sub(r"#\w+", " ", texto)
    
    tokens = texto.split()
    tokens = [tok for tok in tokens if tok not in STOPWORDS_ES and len(tok) > 2]
    
    return " ".join(tokens)

def preprocesar_corpus(df):
    df_clean = df.copy()
    df_clean["texto_limpio"] = df_clean["texto"].apply(limpiar_texto)
    return df_clean