import pandas as pd
import os
import config
import fuentes
import preprocessing
import features
import visualization
import database

def main():
# Comprobar existencia de archivo local
    if os.path.exists(config.RAW_PARQUET_OUTPUT):
        print("Cargando corpus crudo desde archivo local...")
        df_corpus = pd.read_parquet(config.RAW_PARQUET_OUTPUT)
    else:
        # 1. Adquisicion
        print("Extrayendo datos de X...")
        df_x = fuentes.buscar_posts_x(config.X_QUERY, config.X_BEARER_TOKEN, config.X_MAX_RESULTS)

        print("Extrayendo RSS Cooperativa...")
        df_coop = fuentes.leer_rss(config.COOPERATIVA_RSS_URL, "cooperativa", config.COOPERATIVA_MAX_ITEMS)

        print("Extrayendo RSS La Tercera...")
        df_lt = fuentes.leer_rss(config.LATERCERA_RSS_URL, "latercera", config.LATERCERA_MAX_ITEMS)

        # 2. Normalizacion y Consolidacion
        print("Consolidando corpus...")
        df_corpus = pd.concat([df_x, df_coop, df_lt], ignore_index=True)

        df_corpus["texto"] = df_corpus["texto"].fillna("").astype(str)
        df_corpus = df_corpus[df_corpus["texto"].str.strip() != ""].copy()

        # 3. Persistencia Local (Cruda)
        df_corpus.to_parquet(config.RAW_PARQUET_OUTPUT, index=False, compression="snappy")
        print(f"Corpus guardado exitosamente en: {config.RAW_PARQUET_OUTPUT}")

    # 4. Preprocesamiento
    print("Iniciando limpieza de texto...")
    df_limpio = preprocessing.preprocesar_corpus(df_corpus)

    # Persistencia Local (Procesada)
    df_limpio.to_parquet(config.PROCESSED_PARQUET_OUTPUT, index=False, compression="snappy")
    print(f"Corpus limpio guardado en: {config.PROCESSED_PARQUET_OUTPUT}")

    # 5. Capa de Análisis Vectorial y Clustering
    print("Aplicando TF-IDF, K-Means y PCA...")
    df_final, vectorizador, modelo_kmeans = features.extraer_caracteristicas_y_clusters(df_limpio)
    
    print("\nTérminos más representativos por cluster:")
    features.imprimir_top_terminos_cluster(modelo_kmeans, vectorizador)

    # Persistencia Local
    df_final.to_parquet(config.FINAL_PARQUET_OUTPUT, index=False, compression="snappy")
    print(f"Análisis completado. Datos finales guardados en: {config.FINAL_PARQUET_OUTPUT}")
    print(f"Columnas nuevas generadas: {['cluster', 'pca_1', 'pca_2']}")

    # 6. Capa de Visualizacion
    print("Generando gráficos exploratorios...")
    visualization.graficar_top_20_frecuencias(df_final)
    visualization.graficar_pca_por_fuente(df_final)
    visualization.graficar_pca_por_cluster(df_final)

    # 7. Persistencia Externa (MongoDB)
    print("Subiendo datos a MongoDB...")
    database.guardar_en_mongodb(
        df=df_final,
        mongo_uri=config.MONGODB_URI,
        db_name=config.MONGO_DB_NAME,
        collection_name=config.MONGO_COLLECTION_NAME
    )

if __name__ == "__main__":
    main()