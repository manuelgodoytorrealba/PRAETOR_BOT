from playwright.sync_api import TimeoutError
from navegador import iniciar_navegador, cerrar_todo

HOME_URL = "https://www.bstn.com/eu_es/"
URL_PRODUCTO = "https://www.bstn.com/eu_es/p/jordan-air-jordan-12-retro-french-blue-ct8013-114-0335582"

def main():
    playwright, navegador, contexto, pagina, _ = iniciar_navegador(headless=False)

    try:
        # 0) Cargar la home primero y esperar a que termine el tráfico principal
        print("🚀 Abriendo la web...")
        pagina.goto(HOME_URL, timeout=100000, wait_until="domcontentloaded")
        # Espera adicional a que se asienten las peticiones (imágenes, bundles, etc.)
        pagina.wait_for_load_state("networkidle")

        # 1) Pausa para login (ya con la web cargada)
        print("🌐 La web ya cargó. Si necesitas iniciar sesión, hazlo ahora en esta ventana.")
        print("   (Si ya tienes sesión guardada, simplemente presiona Enter para continuar).")
        input("⏳ Presiona Enter cuando quieras continuar con el bot...")

        # 2) Lógica automática: ir al producto, elegir talla y añadir al carrito
        pagina.goto(URL_PRODUCTO, timeout=30000, wait_until="domcontentloaded")
        pagina.wait_for_selector('a[title="US 9 UNSX"]', timeout=15000)
        pagina.click('a[title="US 9 UNSX"]', timeout=5000)
        print("✅ Talla seleccionada")

        pagina.wait_for_selector('button#addToCartButton', timeout=15000)
        pagina.click('button#addToCartButton')
        print("✅ Producto agregado al carrito")

    except TimeoutError as e:
        print(f"❌ Timeout: {e}")

    # 3) Mantener el navegador abierto hasta que decidas cerrar y guardar sesión
    input("🔐 Presiona Enter para guardar la sesión y cerrar el bot...")
    cerrar_todo(playwright, navegador, contexto, guardar_estado=True)

if __name__ == "__main__":
    main()