import json, os, re, urllib.parse, urllib.request

UA = {"User-Agent": "IG-Assessoria-carrossel/1.0 (igorrufinofigueiredo@gmail.com)"}
API = "https://commons.wikimedia.org/w/api.php"
BUSCAS = {
    "magalu": ["Magazine Luiza loja", "Magazine Luiza", "Magalu"],
    "cacaushow": ["Cacau Show loja", "Cacau Show"],
    "weg": ["WEG Jaraguá do Sul", "WEG motor", "WEG S.A."],
    "ifood": ["iFood entregador", "iFood", "entregador bag iFood"],
}


def get(params):
    params = dict(params, format="json")
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers=UA)
    return json.load(urllib.request.urlopen(req, timeout=60))


manifest = {}
for chave, termos in BUSCAS.items():
    os.makedirs(f"fotos/{chave}", exist_ok=True)
    vistos, itens = set(), []
    for termo in termos:
        r = get({"action": "query", "list": "search", "srsearch": termo,
                 "srnamespace": 6, "srlimit": 20})
        for hit in r.get("query", {}).get("search", []):
            t = hit["title"]
            if t in vistos or not re.search(r"\.(jpe?g|png|webp)$", t, re.I):
                continue
            vistos.add(t)
            info = get({"action": "query", "titles": t, "prop": "imageinfo",
                        "iiprop": "url|extmetadata|size", "iiurlwidth": 1600})
            page = next(iter(info["query"]["pages"].values()))
            ii = page.get("imageinfo", [{}])[0]
            meta = ii.get("extmetadata", {})
            url = ii.get("thumburl") or ii.get("url")
            if not url:
                continue
            nome = f"{len(itens):02d}.jpg"
            try:
                req = urllib.request.Request(url, headers=UA)
                with open(f"fotos/{chave}/{nome}", "wb") as f:
                    f.write(urllib.request.urlopen(req, timeout=60).read())
            except Exception as e:
                print("falhou", t, e)
                continue
            itens.append({
                "arquivo": nome, "titulo": t,
                "largura": ii.get("width"), "altura": ii.get("height"),
                "autor": re.sub("<[^>]+>", "", meta.get("Artist", {}).get("value", "")).strip(),
                "licenca": meta.get("LicenseShortName", {}).get("value", ""),
                "descricao": re.sub("<[^>]+>", "", meta.get("ImageDescription", {}).get("value", ""))[:200],
                "pagina": ii.get("descriptionurl"),
            })
            if len(itens) >= 14:
                break
        if len(itens) >= 14:
            break
    manifest[chave] = itens
    print(chave, len(itens))

with open("fotos/manifest.json", "w") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=1)
