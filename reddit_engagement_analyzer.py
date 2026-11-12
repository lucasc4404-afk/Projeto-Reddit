"""
Script para buscar os 100 posts mais recentes no Reddit sobre 'tecnologia' e 'futebol',
extraindo os 5 posts com maior engajamento (Score + Comentários) de cada tópico.

Utiliza a API Oficial do Reddit via OAuth2 (Application-Only / Client Credentials).
"""

import base64
import datetime
import json
import os
import sys
import time
import urllib.parse
import urllib.request

# Configuração das credenciais da API do Reddit
# Crie seu app em: https://www.reddit.com/prefs/apps (tipo 'script')
CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID", "SEU_CLIENT_ID_AQUI")
CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET", "SEU_CLIENT_SECRET_AQUI")
USER_AGENT = "python:reddit_top_engagement:v1.0 (by /u/seu_usuario)"

def get_access_token(client_id: str, client_secret: str) -> str:
    """Obtém um token de acesso OAuth2 usando client_credentials."""
    auth_str = f"{client_id}:{client_secret}"
    b64_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
    
    token_url = "https://www.reddit.com/api/v1/access_token"
    data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode("utf-8")
    
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "User-Agent": USER_AGENT
    }
    
    req = urllib.request.Request(token_url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            return res_json.get("access_token")
    except Exception as e:
        print(f"[!] Erro ao autenticar na API do Reddit: {e}")
        return None

def fetch_posts(token: str, query: str, limit: int = 100) -> list:
    """Busca posts recentes usando a API OAuth oficial do Reddit."""
    posts = []
    after = None
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": USER_AGENT
    }

    print(f"[*] Buscando posts recentes para o tópico: '{query}'...")
    
    while len(posts) < limit:
        batch_limit = min(100, limit - len(posts))
        params = {
            "q": query,
            "sort": "new",
            "limit": batch_limit
        }
        if after:
            params["after"] = after

        url = f"https://oauth.reddit.com/search?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"[!] Falha na requisição para '{query}': {e}")
            break

        children = data.get("data", {}).get("children", [])
        if not children:
            break

        for item in children:
            p = item.get("data", {})
            score = p.get("score", 0)
            comments = p.get("num_comments", 0)
            
            post_info = {
                "id": p.get("id"),
                "title": p.get("title"),
                "subreddit": p.get("subreddit_name_prefixed", f"r/{p.get('subreddit')}"),
                "author": p.get("author"),
                "score": score,
                "num_comments": comments,
                "engagement": score + comments,  # Métrica de engajamento
                "created_utc": p.get("created_utc"),
                "created_at": datetime.datetime.fromtimestamp(p.get("created_utc", 0), tz=datetime.timezone.utc).strftime("%d/%m/%Y %H:%M:%S UTC"),
                "permalink": f"https://www.reddit.com{p.get('permalink')}",
                "url": p.get("url")
            }
            posts.append(post_info)

        after = data.get("data", {}).get("after")
        if not after or len(posts) >= limit:
            break

        time.sleep(1)  # Respeita o rate limit da API

    print(f"[+] Total de posts coletados para '{query}': {len(posts)}")
    return posts[:limit]

def main():
    if CLIENT_ID == "SEU_CLIENT_ID_AQUI" or CLIENT_SECRET == "SEU_CLIENT_SECRET_AQUI":
        print("\n" + "="*80)
        print("ATENÇÃO: É necessário configurar o CLIENT_ID e CLIENT_SECRET da API do Reddit.")
        print("Você pode preencher as variáveis no código ou definir as variáveis de ambiente:")
        print("  REDDIT_CLIENT_ID e REDDIT_CLIENT_SECRET")
        print("Como obter: acesse https://www.reddit.com/prefs/apps e crie um app do tipo 'script'.")
        print("="*80 + "\n")
        return

    print("[*] Autenticando com a API do Reddit...")
    token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    if not token:
        print("[!] Não foi possível obter o token de acesso. Verifique suas credenciais.")
        return

    topics = ["tecnologia", "futebol"]
    results = {}

    for topic in topics:
        posts = fetch_posts(token, topic, limit=100)
        
        # Salva o dump com os 100 posts recentes coletados
        output_file = f"{topic}_100_recentes.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        print(f"[*] Os 100 posts recentes de '{topic}' foram salvos em: {output_file}")

        # Ordena os posts pelo total de engajamento (Score + Comentários)
        top5 = sorted(posts, key=lambda x: (x["engagement"], x["score"], x["num_comments"]), reverse=True)[:5]
        results[topic] = top5

    # Salva os Top 5 de cada tópico
    with open("top5_engajamento_por_topico.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Exibição dos resultados formatados
    print("\n" + "="*80)
    print("TOP 5 POSTS COM MAIOR ENGAJAMENTO (DE CADA TÓPICO)")
    print("="*80)

    for topic, top5 in results.items():
        print(f"\n==================== TÓPICO: {topic.upper()} ====================")
        for idx, post in enumerate(top5, 1):
            print(f"\n#{idx} - {post['title']}")
            print(f"     Comunidade: {post['subreddit']} | Autor: u/{post['author']}")
            print(f"     Engajamento: {post['engagement']} (Upvotes: {post['score']} | Comentários: {post['num_comments']})")
            print(f"     Publicado em: {post['created_at']}")
            print(f"     Link: {post['permalink']}")

if __name__ == "__main__":
    main()
