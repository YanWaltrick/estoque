import os
import sys
import time
import threading
import webbrowser
from app import app

def open_browser():
    """Abre o navegador após um pequeno delay"""
    time.sleep(2)  # Espera o servidor iniciar
    webbrowser.open('http://localhost:5000')

def main():
    """Função principal para executar o aplicativo"""
    # Inicia thread para abrir navegador
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    # Executa o servidor Flask
    print("Iniciando Sistema de Estoque...")
    print("Abrindo navegador em http://localhost:5000")
    print("Pressione Ctrl+C para parar o servidor")

    app.run(host='127.0.0.1', port=5000, debug=False)

if __name__ == '__main__':
    main()