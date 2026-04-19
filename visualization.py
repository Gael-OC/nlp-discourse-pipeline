import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter


def graficar_top_20_frecuencias(df):
    if len(df) == 0 or "texto_limpio" not in df.columns:
        return
        
    # Conteo global de palabras
    todas = " ".join(df["texto_limpio"].astype(str)).split()
    frecuencias = Counter(todas)
    top_20 = pd.DataFrame(frecuencias.most_common(20), columns=["palabra", "frecuencia"])
    
    # Grafico de barras
    plt.figure(figsize=(12, 5))
    plt.bar(top_20["palabra"], top_20["frecuencia"])
    plt.title("Top 20 palabras más frecuentes del corpus")
    plt.xlabel("Palabra")
    plt.ylabel("Frecuencia")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def graficar_pca_por_fuente(df):
    if len(df) == 0 or "pca_1" not in df.columns:
        return
        
    # Dispersion 2D coloreada por origen
    plt.figure(figsize=(8, 6))
    for fuente in df["fuente"].unique():
        subset = df[df["fuente"] == fuente]
        plt.scatter(subset["pca_1"], subset["pca_2"], label=fuente, alpha=0.7)
        
    plt.title("PCA del corpus coloreado por fuente")
    plt.xlabel("Componente principal 1")
    plt.ylabel("Componente principal 2")
    plt.legend()
    plt.tight_layout()
    plt.show()

def graficar_pca_por_cluster(df):
    if len(df) == 0 or "cluster" not in df.columns:
        return
        
    # Dispersion 2D coloreada por grupo K-Means
    plt.figure(figsize=(8, 6))
    for cluster_id in sorted(df["cluster"].unique()):
        subset = df[df["cluster"] == cluster_id]
        plt.scatter(subset["pca_1"], subset["pca_2"], label=f"Cluster {cluster_id}", alpha=0.7)
        
    plt.title("PCA del corpus coloreado por cluster")
    plt.xlabel("Componente principal 1")
    plt.ylabel("Componente principal 2")
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    