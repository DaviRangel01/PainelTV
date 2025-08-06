#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Execução Automática - Painel TV
Executa a captura de telas a cada 30 minutos automaticamente
"""

import schedule
import time
import subprocess
import sys
import logging
from datetime import datetime
import os

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/execucao_automatica.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def executar_captura():
    """Executa o script de captura de telas"""
    try:
        logger.info("🚀 Iniciando captura automática...")
        
        # Executar script de captura
        resultado = subprocess.run(
            [sys.executable, 'captura_telas.py'],
            capture_output=True,
            text=True,
            timeout=600  # Timeout de 10 minutos
        )
        
        if resultado.returncode == 0:
            logger.info("✅ Captura executada com sucesso")
            logger.debug(f"Output: {resultado.stdout}")
        else:
            logger.error(f"❌ Erro na captura. Código: {resultado.returncode}")
            logger.error(f"Erro: {resultado.stderr}")
            
    except subprocess.TimeoutExpired:
        logger.error("⏰ Timeout na execução da captura")
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {str(e)}")

def verificar_sistema():
    """Verifica se o sistema está funcionando"""
    try:
        # Verificar se pasta de avisos existe e tem conteúdo
        pasta_avisos = 'avisos'
        if not os.path.exists(pasta_avisos):
            logger.warning("⚠️ Pasta de avisos não existe")
            return False
            
        arquivos = [f for f in os.listdir(pasta_avisos) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        
        logger.info(f"📊 Status: {len(arquivos)} avisos na pasta")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao verificar sistema: {str(e)}")
        return False

def main():
    """Função principal do sistema automático"""
    print("=" * 60)
    print("🤖 SISTEMA AUTOMÁTICO - PAINEL TV")
    print("=" * 60)
    
    logger.info("Sistema automático iniciado")
    
    # Verificar sistema inicialmente
    if not verificar_sistema():
        logger.warning("⚠️ Sistema pode estar com problemas")
    
    # Executar uma captura inicial
    logger.info("🎯 Executando captura inicial...")
    executar_captura()
    
    # Agendar execuções
    schedule.every(30).minutes.do(executar_captura)
    schedule.every().hour.do(verificar_sistema)
    
    logger.info("⏰ Agendamento configurado: captura a cada 30 minutos")
    logger.info("🔄 Sistema em execução... (Ctrl+C para parar)")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verificar a cada minuto
            
    except KeyboardInterrupt:
        logger.info("⚠️ Sistema interrompido pelo usuário")
        print("\n👋 Sistema parado. Até mais!")
    except Exception as e:
        logger.error(f"❌ Erro no sistema automático: {str(e)}")

if __name__ == "__main__":
    main()