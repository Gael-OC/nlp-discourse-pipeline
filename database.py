import json
from datetime import datetime, timezone
from pymongo import MongoClient

def guardar_en_mongodb(df, mongo_uri, db_name, collection_name):
    if not mongo_uri:
        print("No se ingresó URI de MongoDB. Se omite el guardado.")
        return

    if len(df) == 0:
        print("El DataFrame está vacío. No hay datos para guardar.")
        return

    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    fecha_carga = datetime.now(timezone.utc).isoformat()

    for _, row in df.iterrows():
        documento = row.to_dict()

        # Llave unica estable para evitar duplicados en la base de datos
        documento["_id"] = f"{documento['fuente']}::{documento['id']}"
        documento["fecha_carga_utc"] = fecha_carga

        collection.update_one(
            {"_id": documento["_id"]},
            {"$set": documento},
            upsert=True
        )

    print(f"Datos guardados/actualizados en MongoDB: {db_name}.{collection_name}")