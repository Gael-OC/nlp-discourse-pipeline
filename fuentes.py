import pandas as pd
import requests
import feedparser

def leer_rss(url_rss, nombre_fuente, max_items=20):
    feed = feedparser.parse(url_rss)
    registros = []

    for i, entry in enumerate(feed.entries[:max_items], start=1):
        titulo = entry.get("title", "")
        resumen = entry.get("summary", "")
        
        # Se unen para dar mas contexto al algoritmo
        texto = f"{titulo}. {resumen}".strip()

        registros.append({
            "id": f"{nombre_fuente}_{i}",
            "fuente": nombre_fuente,
            "texto": texto,
            "fecha": entry.get("published", entry.get("updated", None)),
            "url": entry.get("link", ""),
            "autor": entry.get("author", None),
            "consulta": None
        })

    return pd.DataFrame(registros)


def buscar_posts_x(query, bearer_token, max_results=10):
    # Retorno temprano si no hay token
    if not bearer_token:
        return pd.DataFrame(columns=["id", "fuente", "texto", "fecha", "url", "autor", "consulta"])

    url = "https://api.x.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    params = {
        "query": query,
        "max_results": max(10, min(max_results, 100)),
        "tweet.fields": "created_at,author_id,lang",
        "expansions": "author_id",
        "user.fields": "username,name"
    }

    response = requests.get(url, headers=headers, params=params, timeout=30)

    # Manejo de error HTTP
    if response.status_code != 200:
        return pd.DataFrame(columns=["id", "fuente", "texto", "fecha", "url", "autor", "consulta"])

    data = response.json()
    posts = data.get("data", [])
    users = data.get("includes", {}).get("users", [])
    
    # Mapeo rapido de ID a nombre de usuario
    user_map = {u["id"]: u.get("username", "") for u in users}

    registros = []
    for post in posts:
        post_id = post.get("id", "")
        author_id = post.get("author_id", "")
        username = user_map.get(author_id, "")

        registros.append({
            "id": post_id,
            "fuente": "x",
            "texto": post.get("text", ""),
            "fecha": post.get("created_at"),
            "url": f"https://x.com/{username}/status/{post_id}" if username and post_id else None,
            "autor": username if username else author_id,
            "consulta": query
        })

    return pd.DataFrame(registros)