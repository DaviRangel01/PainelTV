#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Captura de Telas - Painel TV
Autor: Sistema Automatizado
Data: 2025

Este script faz login no site operacional da Movecta, navega pelas páginas
e captura screenshots das tabelas para exibição no painel da TV.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
from datetime import datetime
import logging

class CapturaTelaMovecta:
    def __init__(self):
        """Inicializa o capturador de telas"""
        
        # Configurações do site (MOVER PARA ARQUIVO CONFIG.JSON DEPOIS)
        self.url_base = "https://operacional.novvsitj.movecta.com.br/"
        self.usuario = "matheus.costa"
        self.senha = "11012023Ll!"
        
        # Configurações dos diretórios
        self.pasta_avisos = "avisos"
        self.pasta_screenshots = "screenshots_temp"
        
        # Criar pastas se não existirem
        self.criar_pastas()
        
        # Configurar logging
        self.configurar_logging()
        
        # Driver do navegador
        self.driver = None
        
        # URLs das páginas que queremos capturar (exemplos - ajustar conforme necessário)
        self.urls_captura = [
            f"{self.url_base}",  # Página inicial após login
            f"{self.url_base}dashboard",  # Se existir
            f"{self.url_base}relatorios",  # Se existir
            f"{self.url_base}tabelas",    # Se existir
            # Adicione as URLs reais das páginas com tabelas que você quer capturar
        ]
    
    def criar_pastas(self):
        """Cria as pastas necessárias se não existirem"""
        for pasta in [self.pasta_avisos, self.pasta_screenshots]:
            if not os.path.exists(pasta):
                os.makedirs(pasta)
                print(f"📁 Pasta criada: {pasta}")
    
    def configurar_logging(self):
        """Configura o sistema de logs"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('captura_log.txt'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def inicializar_navegador(self):
        """Inicializa o navegador Chrome em modo headless"""
        try:
            chrome_options = Options()
            
            # Configurações para executar em segundo plano (headless)
            chrome_options.add_argument('--headless')  # Remove para ver o navegador funcionando
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')  # Resolução para screenshots
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            
            # Inicializar o driver
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()
            
            self.logger.info("🌐 Navegador inicializado com sucesso")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao inicializar navegador: {str(e)}")
            return False
    
    def fazer_login(self):
        """Realiza o login no site da Movecta"""
        try:
            self.logger.info("🔐 Iniciando processo de login...")
            
            # Navegar para a página de login
            self.driver.get(self.url_base)
            
            # Aguardar a página carregar
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Procurar campos de login (ajustar seletores conforme necessário)
            # Seletores específicos para o site da Movecta
            campo_usuario = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "email"))  # Campo de email/usuário
            )
            
            campo_senha = self.driver.find_element(By.ID, "password")  # Campo de senha
            
            # Preencher credenciais
            campo_usuario.clear()
            campo_usuario.send_keys(self.usuario)
            
            campo_senha.clear()
            campo_senha.send_keys(self.senha)
            
            # Encontrar e clicar no botão de login
            botao_login = self.driver.find_element(By.XPATH, "//button[contains(@class, 'btn') or @type='submit']")
            botao_login.click()
            
            # Aguardar o login ser processado
            time.sleep(8)
            
            # Verificar se login foi bem-sucedido (ajustar conforme necessário)
            if "operacional.novvsitj.movecta.com.br" in self.driver.current_url and "login" not in self.driver.current_url:
                self.logger.info("✅ Login realizado com sucesso")
                return True
            else:
                self.logger.error(f"❌ Falha no login - URL atual: {self.driver.current_url}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erro durante o login: {str(e)}")
            return False
    
    def aguardar_tabelas_carregar(self):
        """Aguarda as tabelas carregarem completamente (10 segundos conforme especificado)"""
        self.logger.info("⏳ Aguardando tabelas carregarem (10 segundos)...")
        time.sleep(10)
        
        # Aguardar elementos específicos das tabelas aparecerem
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            self.logger.info("📊 Tabelas carregadas")
        except:
            self.logger.warning("⚠️ Não foi possível detectar tabelas, mas continuando...")
    
    def capturar_screenshot(self, nome_arquivo):
        """Captura screenshot da página atual"""
        try:
            # Aguardar tabelas carregarem
            self.aguardar_tabelas_carregar()
            
            # Rolar para o topo da página para captura completa
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            # Gerar timestamp para nome único
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_completo = f"{nome_arquivo}_{timestamp}.png"
            
            # Caminho completo do arquivo
            caminho_screenshot = os.path.join(self.pasta_screenshots, nome_completo)
            
            # Capturar screenshot
            self.driver.save_screenshot(caminho_screenshot)
            
            # Copiar para pasta de avisos (onde o painel vai ler)
            caminho_aviso = os.path.join(self.pasta_avisos, nome_completo)
            
            # Copiar arquivo
            import shutil
            shutil.copy2(caminho_screenshot, caminho_aviso)
            
            self.logger.info(f"📸 Screenshot capturado: {nome_completo}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao capturar screenshot: {str(e)}")
            return False
    
    def navegar_e_capturar(self, url, nome_pagina):
        """Navega para uma URL específica e captura screenshot"""
        try:
            self.logger.info(f"🔗 Navegando para: {url}")
            
            self.driver.get(url)
            
            # Aguardar página carregar
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Capturar screenshot
            return self.capturar_screenshot(nome_pagina)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao navegar para {url}: {str(e)}")
            return False
    
    def limpar_screenshots_antigos(self, dias_manter=1):
        """Remove screenshots mais antigos que X dias"""
        try:
            import glob
            import time
            
            # Limpar pasta de screenshots temporários
            arquivos = glob.glob(os.path.join(self.pasta_screenshots, "*.png"))
            arquivos_removidos = 0
            
            for arquivo in arquivos:
                idade_arquivo = time.time() - os.path.getmtime(arquivo)
                if idade_arquivo > (dias_manter * 24 * 3600):  # Converter dias para segundos
                    os.remove(arquivo)
                    arquivos_removidos += 1
            
            # Limpar pasta de avisos (manter apenas screenshots recentes)
            arquivos_avisos = glob.glob(os.path.join(self.pasta_avisos, "*_2024*.png"))  # Screenshots automáticos
            for arquivo in arquivos_avisos:
                idade_arquivo = time.time() - os.path.getmtime(arquivo)
                if idade_arquivo > (dias_manter * 24 * 3600):
                    os.remove(arquivo)
                    arquivos_removidos += 1
            
            if arquivos_removidos > 0:
                self.logger.info(f"🗑️ Removidos {arquivos_removidos} screenshots antigos")
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao limpar screenshots antigos: {str(e)}")
    
    def executar_captura_completa(self):
        """Executa o processo completo de captura"""
        self.logger.info("🚀 Iniciando captura completa...")
        
        try:
            # Inicializar navegador
            if not self.inicializar_navegador():
                return False
            
            # Fazer login
            if not self.fazer_login():
                return False
            
            # Aguardar sistema estabilizar após login
            time.sleep(3)
            
            # Capturar screenshot da página inicial (dashboard)
            self.capturar_screenshot("dashboard_inicial")
            
            # Navegar e capturar outras páginas
            paginas_capturar = [
                {"url": f"{self.url_base}relatorios", "nome": "relatorios"},
                {"url": f"{self.url_base}operacional", "nome": "operacional"},
                {"url": f"{self.url_base}dashboard", "nome": "dashboard_detalhado"},
                # Adicione mais páginas conforme necessário
            ]
            
            for pagina in paginas_capturar:
                self.navegar_e_capturar(pagina["url"], pagina["nome"])
                time.sleep(3)  # Pausa entre capturas
            
            # Limpar screenshots antigos
            self.limpar_screenshots_antigos()
            
            self.logger.info("✅ Captura completa finalizada com sucesso!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro durante captura completa: {str(e)}")
            return False
            
        finally:
            # Fechar navegador
            if self.driver:
                self.driver.quit()
                self.logger.info("🌐 Navegador fechado")

def main():
    """Função principal"""
    print("=" * 60)
    print("🖥️  SISTEMA DE CAPTURA DE TELAS - PAINEL TV")
    print("=" * 60)
    
    capturador = CapturaTelaMovecta()
    
    try:
        sucesso = capturador.executar_captura_completa()
        
        if sucesso:
            print("\n✅ Processo concluído com sucesso!")
            print(f"📁 Screenshots salvos em: {capturador.pasta_avisos}")
            print("🔄 Execute novamente em 30 minutos para atualização")
        else:
            print("\n❌ Processo finalizado com erros. Verifique o log.")
            
    except KeyboardInterrupt:
        print("\n⚠️ Processo interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")

if __name__ == "__main__":
    main()