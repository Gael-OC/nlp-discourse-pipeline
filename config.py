from getpass import getpass

# Credenciales
X_BEARER_TOKEN = getpass("Ingresa tu Bearer Token de X: ")
MONGODB_URI = getpass("Ingresa tu URI de MongoDB: ")

# Parametros de busqueda en X
X_QUERY = (
    '((Chile OR chileno OR chilena OR gobierno OR congreso OR senado OR diputados OR presidencia OR presidente OR ministra OR ministerio OR "La Moneda" OR elecciones OR plebiscito OR constitución) (política OR politico OR politica OR gobierno OR legislativo OR ejecutivo)) '
    'OR ((internacional OR mundo OR geopolítica OR geopolitica OR diplomacia OR ONU OR OTAN OR "Estados Unidos" OR Rusia OR Ucrania OR China OR Europa OR Israel OR Gaza) (política OR politico OR politica OR elecciones OR gobierno OR conflicto OR guerra OR sanciones)) '
    'lang:es has:links -is:retweet -is:reply'
)
X_MAX_RESULTS = 500

# Parametros RSS
COOPERATIVA_RSS_URL = "https://www.cooperativa.cl/noticias/site/tax/port/all/rss_3___1.xml"
COOPERATIVA_MAX_ITEMS = 25

LATERCERA_RSS_URL = "https://www.latercera.com/arc/outboundfeeds/rss/?outputType=xml"
LATERCERA_MAX_ITEMS = 25

# Configuracion MongoDB
MONGO_DB_NAME = "LaboratorioML"
MONGO_COLLECTION_NAME = "corpus_textos"

# Salidas de archivos binarios
RAW_PARQUET_OUTPUT = "data/raw/corpus_crudo.parquet"
PROCESSED_PARQUET_OUTPUT = "data/processed/corpus_limpio.parquet"
PICKLE_OUTPUT_NAME = "data/processed/corpus_consolidado_laboratorio_01.pkl"
FINAL_PARQUET_OUTPUT = "data/processed/corpus_final_clusterizado.parquet"