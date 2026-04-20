import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.feature_selection import VarianceThreshold
import umap.umap_ as umap

def obtener_frecuencias(textos):
    todas = " ".join(textos).split()
    return Counter(todas)

def extraer_caracteristicas_y_clusters(df):
    df_out = df.copy()
    if len(df_out) == 0:
        return df_out, None, None

    # Vectorizacion TF-IDF
    vectorizer = TfidfVectorizer(max_features=1000)
    X_tfidf = vectorizer.fit_transform(df_out["texto_limpio"])

    # Seleccion de caracteristicas
    selector = VarianceThreshold(threshold=0.0001)
    X_sel = selector.fit_transform(X_tfidf)

    # Agrupamiento
    k = 4 if len(df_out) >= 4 else max(1, len(df_out))
    modelo_kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df_out["cluster"] = modelo_kmeans.fit_predict(X_sel)

    if len(df_out) >= 2:
        X_dense = X_tfidf.toarray()
        
        # PCA
        pca = PCA(n_components=2, random_state=42)
        X_pca = pca.fit_transform(X_dense)
        df_out["pca_1"] = X_pca[:, 0]
        df_out["pca_2"] = X_pca[:, 1]

        # t-SNE
        tsne = TSNE(n_components=2, perplexity=10, random_state=42, init='pca')
        X_tsne = tsne.fit_transform(X_dense)
        df_out["tsne_1"] = X_tsne[:, 0]
        df_out["tsne_2"] = X_tsne[:, 1]

        # UMAP
        reductor = umap.UMAP(n_neighbors=10, min_dist=0.1, n_components=2, random_state=42)
        X_umap = reductor.fit_transform(X_dense)
        df_out["umap_1"] = X_umap[:, 0]
        df_out["umap_2"] = X_umap[:, 1]
    else:
        for col in ["pca_1", "pca_2", "tsne_1", "tsne_2", "umap_1", "umap_2"]:
            df_out[col] = 0.0

    return df_out, vectorizer, modelo_kmeans

def imprimir_top_terminos_cluster(modelo_kmeans, vectorizer, top_n=10):
    terminos = vectorizer.get_feature_names_out()
    for i, centroide in enumerate(modelo_kmeans.cluster_centers_):
        indices = centroide.argsort()[::-1][:top_n]
        top_terminos = [terminos[idx] for idx in indices]
        print(f"Cluster {i}: {top_terminos}")