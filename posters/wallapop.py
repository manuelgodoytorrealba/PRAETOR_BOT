from playwright.sync_api import sync_playwright

# ✅ Ruta al perfil real de tu navegador Chrome
# Asegúrate de que Chrome esté cerrado antes de ejecutar este script
USER_PROFILE_PATH = "/Users/home/Library/Application Support/Google/Chrome/Default"

with sync_playwright() as p:
    # ✅ Inicia Chrome con tu perfil de usuario real
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_PROFILE_PATH,
        headless=False,  # Muestra el navegador para que puedas iniciar sesión
        args=[
            "--disable-blink-features=AutomationControlled",  # Evita que detecten que es un bot
            "--start-maximized"
        ]
    )

    # ✅ Abre una nueva pestaña en el contexto
    page = context.new_page()

    # ✅ Abre la página de publicación de Wallapop
    page.goto("https://es.wallapop.com/app/catalog/upload")
    page.wait_for_timeout(15000000)

    # ✅ Espera 30 segundos para que puedas iniciar sesión manualmente
    page.wait_for_timeout(30000000)

   