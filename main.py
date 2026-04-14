import pandas as pd
import config
import fuentes

def main():
    # 1. Capa de Adquisicion
    print("Extrayendo datos de X...")
    df_x = fuentes.buscar_posts_x(
        config.X_QUERY, 
        config.X_BEARER_TOKEN, 
        config.X_MAX_RESULTS
    )

    print("Extrayendo RSS Cooperativa...")
    df_coop = fuentes.leer_rss(
        config.COOPERATIVA_RSS_URL, 
        "cooperativa", 
        config.COOPERATIVA_MAX_ITEMS
    )

    print("Extrayendo RSS La Tercera...")
    df_lt = fuentes.leer_rss(
        config.LATERCERA_RSS_URL, 
        "latercera", 
        config.LATERCERA_MAX_ITEMS
    )

    # 2. Capa de Normalizacion y Consolidacion
    print("Consolidando corpus...")
    df_corpus = pd.concat([df_x, df_coop, df_lt], ignore_index=True)

    # Limpieza de documentos sin texto util
    df_corpus["texto"] = df_corpus["texto"].fillna("").astype(str)
    df_corpus = df_corpus[df_corpus["texto"].str.strip() != ""].copy()

    # 3. Capa de Persistencia Local
    df_corpus.to_parquet(config.PARQUET_OUTPUT_NAME, index=False, compression="snappy")
    print(f"Corpus guardado exitosamente en: {config.PARQUET_OUTPUT_NAME}")
    print(f"Total de documentos consolidados: {len(df_corpus)}")

if __name__ == "__main__":
    main()