import os
import json
import subprocess

# Rutas
JSON_PATH = "data/productos.json"
ORIGINAL_FOLDER = "fotos_originales"
OUTPUT_FOLDER = "fotos"

# Cargar productos
with open(JSON_PATH, "r") as f:
    productos = json.load(f)

# Crear carpeta de salida si no existe
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for producto in productos:
    sku = producto["sku"]
    slug = sku.lower().replace("-", "_")
    carpeta_origen = os.path.join(ORIGINAL_FOLDER, slug)

    print(f"\n📦 SKU: {sku}")
    print(f"📂 Buscando en: {carpeta_origen}")

    if not os.path.isdir(carpeta_origen):
        print(f"⚠️  Carpeta no encontrada para {sku}, saltando...")
        continue

    heic_files = [f for f in os.listdir(carpeta_origen) if f.lower().endswith(".heic")]
    heic_files.sort()

    if not heic_files:
        print(f"⚠️  No hay fotos HEIC en {carpeta_origen}")
        continue

    nuevas_rutas = []

    for idx, file in enumerate(heic_files, 1):
        ruta_original = os.path.join(carpeta_origen, file)
        nombre_salida = f"{slug}_{idx}.jpg"
        ruta_salida = os.path.join(OUTPUT_FOLDER, nombre_salida)

        if os.path.exists(ruta_salida):
            print(f"✔️ Ya existe: {nombre_salida} (omitido)")
        else:
            subprocess.run([
                "sips", "-s", "format", "jpeg", ruta_original, "--out", ruta_salida
            ], check=True)
            print(f"✅ Convertido: {file} → {nombre_salida}")

        nuevas_rutas.append(f"fotos/{nombre_salida}")

    producto["fotos"] = nuevas_rutas

# Guardar JSON actualizado
with open(JSON_PATH, "w") as f:
    json.dump(productos, f, indent=2, ensure_ascii=False)

print("\n🎉 Conversión finalizada y JSON actualizado con éxito.")

# ------------------------------------------
# ✅ VERIFICACIÓN FINAL DE FOTOS GENERADAS
# ------------------------------------------

print("\n🔍 Verificando rutas de imágenes en productos.json...")

errores_encontrados = False  # Bandera para saber si hubo errores

for producto in productos:
    sku = producto["sku"]
    fotos = producto.get("fotos", [])

    faltantes = []
    for ruta in fotos:
        # Verifica que el archivo realmente exista en el sistema
        if not os.path.exists(ruta):
            faltantes.append(ruta)

    print(f"\n📦 {sku} — {len(fotos)} fotos registradas")

    if faltantes:
        errores_encontrados = True
        print("❌ Faltan los siguientes archivos:")
        for falta in faltantes:
            print(f"   ⛔ {falta}")
    else:
        print("✅ Todas las rutas de imagen existen correctamente.")

# Mensaje final de estado
if errores_encontrados:
    print("\n⚠️  Se detectaron errores. Revisa las rutas indicadas.")
else:
    print("\n🎯 Verificación completada sin errores. ¡Todo está en orden!")