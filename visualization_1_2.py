import matplotlib.pyplot as plt
from wordcloud import WordCloud

def visualizar_comparativa_estrategias(df):
    if len(df) == 0 or "pca_1" not in df.columns:
        return

    # Subgraficos
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    
    # PCA
    axes[0].scatter(df['pca_1'], df['pca_2'], c=df['cluster'], cmap='viridis', alpha=0.7)
    axes[0].set_title('PCA: Estructura Global Lineal')
    axes[0].set_xlabel('PC1')
    axes[0].set_ylabel('PC2')

    # t-SNE
    axes[1].scatter(df['tsne_1'], df['tsne_2'], c=df['cluster'], cmap='viridis', alpha=0.7)
    axes[1].set_title('t-SNE: Estructura Local (Perplexity=10)')
    axes[1].set_xlabel('Dim 1')
    axes[1].set_ylabel('Dim 2')

    # UMAP
    axes[2].scatter(df['umap_1'], df['umap_2'], c=df['cluster'], cmap='viridis', alpha=0.7)
    axes[2].set_title('UMAP: Equilibrio Local-Global')
    axes[2].set_xlabel('Dim 1')
    axes[2].set_ylabel('Dim 2')

    plt.tight_layout()
    plt.show()

def graficar_nubes_de_palabras(df):
    if len(df) == 0 or "cluster" not in df.columns:
        return

    for cluster_id in sorted(df["cluster"].unique()):
        textos = " ".join(df[df["cluster"] == cluster_id]["texto_limpio"].astype(str))
        if not textos.strip():
            continue
            
        wc = WordCloud(background_color='white', collocations=False).generate(textos)
        
        plt.figure(figsize=(6, 4))
        plt.imshow(wc, interpolation="bilinear")
        plt.title(f"Cluster {cluster_id}")
        plt.axis("off")
        plt.show()