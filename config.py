from getpass import getpass

# Credenciales
X_BEARER_TOKEN = getpass("Ingresa tu Bearer Token de X: ")
MONGODB_URI = getpass("Ingresa tu URI de MongoDB: ")

# Parametros de busqueda en X
X_QUERY = (
    '((Chile OR gobierno OR congreso OR presidente OR "La Moneda" OR elecciones) (política OR legislativo)) '
    'OR ((internacional OR geopolítica OR ONU OR OTAN OR EEUU OR Rusia OR Ucrania OR Gaza) (política OR conflicto OR guerra)) '
    'lang:es has:links -is:retweet -is:reply'
)
X_MAX_RESULTS = 100 

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
FINAL_PARQUET_OUTPUT = "data/processed/corpus_final_clusterizado.parquet"