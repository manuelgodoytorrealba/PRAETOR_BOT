import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'productos.json')

def load_productos():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_productos(productos):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(productos, f, indent=2, ensure_ascii=False)

def get_productos_no_publicados(plataforma):
    productos = load_productos()
    return [p for p in productos if plataforma not in p.get("publicado_en", [])]

def marcar_como_publicado(sku, plataforma):
    productos = load_productos()
    for p in productos:
        if p["sku"] == sku and plataforma not in p.get("publicado_en", []):
            p.setdefault("publicado_en", []).append(plataforma)
    save_productos(productos)