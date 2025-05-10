# Documentação do Perfil GitHub

Este documento explica o funcionamento do repositório do perfil GitHub e como cada componente interage.

## Estrutura do Repositório

```
AspMartins999/
├── .github/
│   └── workflows/
│       └── combined_update.yml  (Workflow unificado)
├── docs/
│   └── documentacao.md         (Esta documentação)
├── utils/
│   ├── cache_manager.py        (Gerenciamento de cache)
│   └── logger.py               (Configuração de logs)
├── .cache/                     (Diretório de cache - criado em runtime)
├── .backups/                   (Backups do README - criado em runtime)
├── README.md                   (Perfil principal)
├── update_readme.py            (Script de atualização)
├── requirements.txt            (Dependências Python)
└── LICENSE                     (Licença MIT)
```

## Componentes Principais

### 1. README.md

Arquivo principal que contém o perfil do GitHub. Possui seções estáticas e dinâmicas marcadas com comentários HTML.

**Seções Dinâmicas:**

- Posts do Blog (`<!--START_SECTION:blog-->`)
- PRs Mesclados (`<!--Start Merged PRs-->`)
- Contagem de PRs (`<!--Start Count Merged PRs-->`)
- Citações (`<!--START_QUOTE-->`)

### 2. update_readme.py

Script Python responsável por atualizar as seções dinâmicas do README. Principais funcionalidades:

- Busca PRs mesclados do usuário via API do GitHub
- Busca posts recentes de blog via feed RSS
- Atualiza dinamicamente o README com essas informações
- Adiciona citações aleatórias
- Implementa cache para reduzir chamadas à API
- Implementa logging para facilitar diagnósticos
- Cria backups do README antes de modificá-lo

### 3. GitHub Actions

#### combined_update.yml (Workflow unificado)

Combina as funcionalidades dos dois workflows anteriores:

- Executa o script Python para atualizar o README
- Gera a animação de "snake" baseada nas contribuições
- Faz push de ambos para a branch `output`

### 4. Sistema de Cache

Implementado em `utils/cache_manager.py`, o sistema de cache:

- Reduz chamadas à API do GitHub
- Armazena resultados em arquivos JSON
- Define tempo de expiração de cache
- Fornece funções para gerenciar os dados em cache

### 5. Sistema de Logs

Implementado em `utils/logger.py`, o sistema de logs:

- Configura logs para console e arquivo
- Permite rastreamento de erros e ações
- Facilita diagnósticos de problemas

## Como Usar

### Executando Atualizações Manualmente

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute o script: `python update_readme.py`

### Personalizações

#### Modificar Citações

Edite a lista `QUOTES` no arquivo `update_readme.py`

#### Alterar Feed do Blog

Atualize a variável `BLOG_RSS` no arquivo `update_readme.py`

#### Alterar Layout

Modifique diretamente o `README.md`, mantendo os comentários delimitadores para as seções dinâmicas

## Manutenção

### Backups

Backups automáticos são gerados no diretório `.backups/` antes de cada atualização

### Logs

Logs são gerados em `update_readme.log` para facilitar o diagnóstico

### Cache

Dados em cache são armazenados em `.cache/github_cache.json`

### Limpeza

#### Arquivos temporários/gerados automaticamente

- `__pycache__/` e arquivos `.pyc` (gerados pelo Python)
- `.backups/` (gerado pelo script durante a execução)
- `.cache/` (gerado pelo script durante a execução)
- `update_readme.log` (gerado pelo script)

#### Script de Limpeza (.gitignore)

```
# Python bytecode
__pycache__/
*.py[cod]

# Logs
*.log

# Backups gerados pelo script
.backups/

# Cache do script
.cache/

# Arquivos temporários do sistema
.DS_Store
Thumbs.db
```

#### Comandos para Executar a Limpeza

```powershell
# Remover diretórios Python cache
Remove-Item -Recurse -Force utils/__pycache__ -ErrorAction SilentlyContinue

# Remover arquivos de log
Remove-Item update_readme.log -ErrorAction SilentlyContinue

# Remover backups e cache (cuidado - se quiser manter backups, não execute)
Remove-Item -Recurse -Force .backups -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .cache -ErrorAction SilentlyContinue
```
