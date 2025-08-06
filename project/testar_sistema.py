import os
import sys
import subprocess
import time
from pathlib import Path

def verificar_estrutura_pastas():
    """Verifica se todas as pastas necessárias existem"""
    print("📁 Verificando estrutura de pastas...")
    
    pastas_necessarias = ['avisos', 'screenshots_temp', 'logs', 'config']
    
    for pasta in pastas_necessarias:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"   ✅ Pasta criada: {pasta}")
        else:
            print(f"   ✅ Pasta existe: {pasta}")

def verificar_arquivos_avisos():
    """Verifica arquivos na pasta de avisos"""
    print("\n🖼️ Verificando avisos...")
    
    pasta_avisos = Path('avisos')
    extensoes = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    
    arquivos = []
    for ext in extensoes:
        arquivos.extend(pasta_avisos.glob(f'*{ext}'))
        arquivos.extend(pasta_avisos.glob(f'*{ext.upper()}'))
    
    if arquivos:
        print(f"   ✅ Encontrados {len(arquivos)} arquivos de imagem:")
        for arquivo in arquivos[:5]:  # Mostrar apenas os primeiros 5
            print(f"      - {arquivo.name}")
        if len(arquivos) > 5:
            print(f"      ... e mais {len(arquivos) - 5} arquivos")
    else:
        print("   ⚠️ Nenhuma imagem encontrada na pasta avisos/")
        print("   💡 Adicione algumas imagens para testar o carrossel")

def testar_servidor():
    """Testa se o servidor consegue iniciar"""
    print("\n🌐 Testando servidor...")
    
    try:
        # Tentar importar módulos necessários
        import http.server
        import socketserver
        print("   ✅ Módulos do servidor disponíveis")
        
        # Testar se porta 8000 está livre
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8000))
        sock.close()
        
        if result == 0:
            print("   ⚠️ Porta 8000 já está em uso")
        else:
            print("   ✅ Porta 8000 disponível")
            
    except ImportError as e:
        print(f"   ❌ Erro de importação: {e}")
        return False
    
    return True

def testar_dependencias_python():
    """Testa dependências do Python"""
    print("\n🐍 Testando dependências Python...")
    
    dependencias = {
        'selenium': 'Automação do navegador',
        'PIL': 'Processamento de imagens (Pillow)',
    }
    
    for modulo, descricao in dependencias.items():
        try:
            __import__(modulo)
            print(f"   ✅ {modulo} - {descricao}")
        except ImportError:
            print(f"   ❌ {modulo} - {descricao} (não instalado)")

def criar_aviso_teste():
    """Cria um aviso de teste se não houver nenhum"""
    print("\n🎨 Criando aviso de teste...")
    
    pasta_avisos = Path('avisos')
    arquivos_existentes = list(pasta_avisos.glob('*.png')) + list(pasta_avisos.glob('*.jpg'))
    
    if not arquivos_existentes:
        # Criar um arquivo HTML simples para gerar aviso
        html_teste = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Teste</title></head>
<body style="margin:0;padding:40px;background:linear-gradient(45deg,#667eea,#764ba2);color:white;font-family:Arial;text-align:center;width:800px;height:400px;display:flex;flex-direction:column;justify-content:center;">
<h1 style="font-size:48px;margin:20px 0;">🖥️ SISTEMA ATIVO</h1>
<p style="font-size:24px;">Painel Digital Funcionando</p>
<p style="font-size:18px;opacity:0.8;">Adicione mais avisos na pasta /avisos/</p>
</body></html>"""
        
        with open('avisos/gerar_aviso_teste.html', 'w', encoding='utf-8') as f:
            f.write(html_teste)
        
        print("   ✅ Arquivo HTML de teste criado em avisos/gerar_aviso_teste.html")
        print("   💡 Abra este arquivo no navegador e capture screenshot")
    else:
        print(f"   ✅ Já existem {len(arquivos_existentes)} avisos")

def main():
    """Função principal de teste"""
    print("=" * 60)
    print("🧪 TESTE DO SISTEMA - PAINEL DIGITAL TV")
    print("=" * 60)
    
    # Verificar estrutura
    verificar_estrutura_pastas()
    
    # Verificar avisos
    verificar_arquivos_avisos()
    
    # Testar servidor
    servidor_ok = testar_servidor()
    
    # Testar dependências
    testar_dependencias_python()
    
    # Criar aviso de teste se necessário
    criar_aviso_teste()
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DO TESTE")
    print("=" * 60)
    
    if servidor_ok:
        print("✅ Sistema básico funcionando")
        print("\n🚀 PRÓXIMOS PASSOS:")
        print("1. Execute: python servidor_arquivos.py")
        print("2. Abra: http://localhost:8000")
        print("3. Adicione imagens na pasta avisos/")
        print("4. Teste captura: python captura_telas.py")
    else:
        print("❌ Sistema com problemas")
        print("\n🔧 CORREÇÕES NECESSÁRIAS:")
        print("1. Reinstale Python completamente")
        print("2. Execute: python instalar_dependencias.py")
        print("3. Execute este teste novamente")

if __name__ == "__main__":
    main()