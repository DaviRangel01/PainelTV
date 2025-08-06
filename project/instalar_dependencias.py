

import subprocess
import sys
import os

def instalar_pip_packages():
    """Instala pacotes Python necessários"""
    print("🐍 Instalando dependências Python...")
    
    packages = [
        'selenium==4.18.1',
        'webdriver-manager==4.0.1',
        'Pillow==10.2.0',
        'python-decouple==3.8',
        'schedule==1.2.0',
        'requests==2.31.0'
    ]
    
    for package in packages:
        try:
            print(f"   Instalando {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"   ✅ {package} instalado")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erro ao instalar {package}: {e}")

def verificar_chrome():
    """Verifica se Chrome está instalado"""
    print("\n🌐 Verificando Google Chrome...")
    
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\%s\AppData\Local\Google\Chrome\Application\chrome.exe" % os.getenv('USERNAME', '')
    ]
    
    chrome_encontrado = False
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"   ✅ Chrome encontrado em: {path}")
            chrome_encontrado = True
            break
    
    if not chrome_encontrado:
        print("   ⚠️ Google Chrome não encontrado!")
        print("   📥 Por favor, baixe e instale o Google Chrome:")
        print("   https://www.google.com/chrome/")

def criar_estrutura_pastas():
    """Cria estrutura de pastas necessária"""
    print("\n📁 Criando estrutura de pastas...")
    
    pastas = ['avisos', 'screenshots_temp', 'logs', 'config']
    
    for pasta in pastas:
        try:
            os.makedirs(pasta, exist_ok=True)
            print(f"   ✅ Pasta criada/verificada: {pasta}")
        except Exception as e:
            print(f"   ❌ Erro ao criar pasta {pasta}: {e}")

def criar_arquivo_config():
    """Cria arquivo de configuração exemplo"""
    print("\n⚙️ Criando arquivo de configuração...")
    
    config_content = """# Arquivo de Configuração - Painel TV
# Mova as credenciais aqui para maior segurança



# Configurações do navegador
MODO_HEADLESS=True
RESOLUCAO_SCREENSHOT=1920x1080

# Configurações de limpeza
MANTER_SCREENSHOTS_DIAS=1
"""
    
    try:
        with open('config/.env', 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("   ✅ Arquivo config/.env criado")
    except Exception as e:
        print(f"   ❌ Erro ao criar config: {e}")

def main():
    """Função principal de instalação"""
    print("=" * 60)
    print("🚀 INSTALADOR - SISTEMA PAINEL DIGITAL TV")
    print("=" * 60)
    
    try:
        # Instalar dependências Python
        instalar_pip_packages()
        
        # Verificar Chrome
        verificar_chrome()
        
        # Criar estrutura de pastas
        criar_estrutura_pastas()
        
        # Criar arquivo de configuração
        criar_arquivo_config()
        
        print("\n" + "=" * 60)
        print("✅ INSTALAÇÃO CONCLUÍDA!")
        print("=" * 60)
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Edite o arquivo 'config/.env' com suas credenciais")
        print("2. Execute 'python captura_telas.py' para testar")
        print("3. Abra 'index.html' no navegador para ver o painel")
        print("4. Configure execução automática no Agendador de Tarefas")
        print("\n🔧 COMANDOS ÚTEIS:")
        print("   python captura_telas.py          # Executa captura manual")
        print("   start index.html                # Abre painel no navegador")
        
    except Exception as e:
        print(f"\n❌ Erro durante instalação: {e}")
        print("💡 Tente executar como Administrador")

if __name__ == "__main__":
    main()