#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor HTTP simples para servir os arquivos do painel
e listar arquivos da pasta de avisos dinamicamente
"""

import http.server
import socketserver
import json
import os
import mimetypes
from urllib.parse import urlparse, parse_qs

class PainelHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handler customizado para o servidor do painel"""
    
    def do_GET(self):
        """Processa requisições GET"""
        parsed_path = urlparse(self.path)
        
        # Endpoint para listar arquivos de avisos
        if parsed_path.path == '/api/avisos':
            self.listar_avisos()
        else:
            # Servir arquivos normalmente
            super().do_GET()
    
    def listar_avisos(self):
        """Lista arquivos da pasta de avisos em formato JSON"""
        try:
            pasta_avisos = 'avisos'
            
            if not os.path.exists(pasta_avisos):
                self.send_json_response({'avisos': [], 'erro': 'Pasta de avisos não encontrada'})
                return
            
            # Listar arquivos de imagem
            extensoes_suportadas = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
            arquivos = []
            
            try:
                for arquivo in os.listdir(pasta_avisos):
                    if arquivo.lower().endswith(extensoes_suportadas):
                        caminho_completo = os.path.join(pasta_avisos, arquivo)
                        
                        # Informações do arquivo
                        stat = os.stat(caminho_completo)
                        
                        arquivos.append({
                            'nome': arquivo,
                            'caminho': f'./avisos/{arquivo}',
                            'tamanho': stat.st_size,
                            'modificado': stat.st_mtime,
                            'url': f'/avisos/{arquivo}'
                        })
            except Exception as e:
                print(f"Erro ao listar arquivos: {e}")
            
            # Ordenar por data de modificação (mais recente primeiro)
            arquivos.sort(key=lambda x: x['modificado'], reverse=True)
            
            resposta = {
                'avisos': arquivos,
                'total': len(arquivos),
                'ultima_atualizacao': max([a['modificado'] for a in arquivos]) if arquivos else 0
            }
            
            self.send_json_response(resposta)
            
        except Exception as e:
            self.send_json_response({
                'avisos': [],
                'erro': f'Erro ao listar avisos: {str(e)}'
            })
    
    def send_json_response(self, data):
        """Envia resposta JSON"""
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(json_data.encode('utf-8'))))
        self.end_headers()
        
        self.wfile.write(json_data.encode('utf-8'))

def iniciar_servidor(porta=8000):
    """Inicia o servidor HTTP"""
    try:
        with socketserver.TCPServer(("", porta), PainelHTTPRequestHandler) as httpd:
            print("=" * 60)
            print("🌐 SERVIDOR PAINEL TV")
            print("=" * 60)
            print(f"🚀 Servidor iniciado na porta {porta}")
            print(f"🔗 Acesse: http://localhost:{porta}")
            print(f"📊 API de avisos: http://localhost:{porta}/api/avisos")
            print("=" * 60)
            print("⚠️  Pressione Ctrl+C para parar o servidor")
            print("=" * 60)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Servidor parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro no servidor: {e}")

if __name__ == "__main__":
    iniciar_servidor()