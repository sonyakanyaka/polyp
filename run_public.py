from globalhost import GlobalHostApp

host = GlobalHostApp()
if host.bg_launch(framework="fastapi", app="app:app", port=8000):
    print(f"Публичный адрес: {host.get_url()}")
    input("Нажмите Enter для остановки...\n")