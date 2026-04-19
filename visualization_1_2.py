from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import umap.umap_ as umap
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.preprocessing import MinMaxScaler
    
def activar_estrategias(df):
    #estrategia PCA
    vectorizer = TfidfVectorizer(max_features=1000)
    X_tfidf = vectorizer.fit_transform(df['texto_limpio'])
    n_docs, n_terms = X_tfidf.shape
    X_dense = X_tfidf.toarray() #TF-IDF 
    pca = PCA(n_components=4, random_state=42)
    X_pca = pca.fit_transform(X_dense)
    df['pca_1'] = X_pca[:, 0]
    df['pca_2'] = X_pca[:, 1]
    
    #XSeleccion 1
    selector = VarianceThreshold(threshold=0.001)
    X_sel = selector.fit_transform(X_dense)
    print('Antes:', X_dense.shape)
    print('Despues:', X_sel.shape)
    
    #Xseleccion 2
    y = df['cluster']
    X_nonneg = MinMaxScaler().fit_transform(X_dense)
    selector = SelectKBest(score_func=chi2, k=20)
    X_best = selector.fit_transform(X_nonneg, y)
    
    
    
    #estrategia T-SNE
    X_emb = TSNE(
    n_components=2,
    perplexity=33,
    learning_rate='auto',
    init='pca',
    random_state=42
    ).fit_transform(X_dense)
    
    
    #estrategia UMAP
    reductor = umap.UMAP(
    n_neighbors=10,
    min_dist=0.15,
    n_components=2,
    random_state=42
    )
    X_umap = reductor.fit_transform(X_dense)
    visualizar_comparativa_estrategias(df, X_dense)
    visualizar_comparativa_estrategias(df, X_sel)
    visualizar_comparativa_estrategias(df, X_best)
    

def visualizar_comparativa_estrategias(df, X_dense):
    # Crear una figura con 3 sub-gráficos alineados
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    
    # --- ESTRATEGIA 1: PCA ---
    axes[0].scatter(df['pca_1'], df['pca_2'], c=df['cluster'], cmap='viridis', alpha=0.7)
    axes[0].set_title('PCA: Estructura Global Lineal')
    axes[0].set_xlabel('PC1')
    axes[0].set_ylabel('PC2')

    # --- ESTRATEGIA 2: t-SNE ---
    X_tsne = TSNE(perplexity=33, random_state=42).fit_transform(X_dense)
    axes[1].scatter(X_tsne[:, 0], X_tsne[:, 1], c=df['cluster'], cmap='viridis', alpha=0.7)
    axes[1].set_title('t-SNE: Estructura Local (Perplexity=33)')

    # --- ESTRATEGIA 3: UMAP ---
    reductor = umap.UMAP(n_neighbors=10, min_dist=0.15, random_state=42)
    X_umap = reductor.fit_transform(X_dense)
    axes[2].scatter(X_umap[:, 0], X_umap[:, 1], c=df['cluster'], cmap='viridis', alpha=0.7)
    axes[2].set_title('UMAP: Equilibrio Local-Global')

    plt.tight_layout()
    plt.show()
    
    