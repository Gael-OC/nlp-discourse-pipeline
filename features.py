import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def obtener_frecuencias(textos):
    todas = " ".join(textos).split()
    return Counter(todas)

def extraer_caracteristicas_y_clusters(df):
    df_out = df.copy()

    if len(df_out) == 0:
        return df_out, None, None

    # TF-IDF
    vectorizer = TfidfVectorizer(max_features=1000)
    X_tfidf = vectorizer.fit_transform(df_out["texto_limpio"])

    # Clustering K-Means
    k = 4 if len(df_out) >= 4 else max(1, len(df_out))
    modelo_kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df_out["cluster"] = modelo_kmeans.fit_predict(X_tfidf)

    # Reduccion de dimensionalidad con PCA
    if len(df_out) >= 2:
        X_dense = X_tfidf.toarray()
        pca = PCA(n_components=2, random_state=42)
        X_pca = pca.fit_transform(X_dense)

        df_out["pca_1"] = X_pca[:, 0]
        df_out["pca_2"] = X_pca[:, 1]
    else:
        df_out["pca_1"] = 0.0
        df_out["pca_2"] = 0.0

    return df_out, vectorizer, modelo_kmeans