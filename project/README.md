# 🖥️ Sistema de Painel Digital para TV

Sistema automatizado para capturar informações de sites e exibi-las em um painel digital na TV.

## 📋 Funcionalidades

- **Captura Automática**: Login automático no site e captura de screenshots das tabelas
- **Painel TV**: Interface em tela cheia para exibição das informações
- **Carrossel Automático**: Troca de avisos a cada 8 segundos
- **Atualização Automática**: Sistema se atualiza a cada 30 minutos
- **Avisos Manuais**: Possibilidade de adicionar imagens personalizadas
- **Interface Responsiva**: Otimizada para diferentes tamanhos de TV

## 🚀 Instalação Rápida

### 1. Executar Instalador
```bash
python instalar_dependencias.py
```

### 2. Configurar Credenciais
Edite o arquivo `config/.env` com suas credenciais do site.

### 3. Testar Sistema
```bash
# Testar captura
python captura_telas.py

# Iniciar servidor
python servidor_arquivos.py
```

### 4. Acessar Painel
Abra no navegador: `http://localhost:8000`

## 🔄 Atualizações Futuras

- [ ] Integração com IA para gerar avisos automáticos
- [ ] Suporte a múltiplos sites
- [ ] Dashboard web para configuração
- [ ] Notificações por email em caso de erro
- [ ] Backup automático de configurações
- [ ] API REST para controle remoto
