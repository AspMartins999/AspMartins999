# Documentação do Perfil GitHub

## Sobre o Repositório

Este repositório contém o perfil personalizado do GitHub para AspMartins999 (Matheus Martins), com atualizações automáticas para manter informações dinâmicas.

## Estrutura do Repositório

```
AspMartins999/
├── .github/
│   └── workflows/
│       └── update_profile.yml    (Workflow para atualizar o README)
├── docs/
│   └── README.md                 (Esta documentação)
├── utils/
│   ├── cache_manager.py          (Gerenciamento de cache)
│   └── logger.py                 (Configuração de logs)
├── .gitignore                    (Configurações para ignorar arquivos)
├── LICENSE                       (Licença do projeto)
├── README.md                     (Perfil principal)
├── requirements.txt              (Dependências Python)
└── update_readme.py              (Script de atualização)
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

#### update_profile.yml (Workflow unificado)

- Executa o script Python para atualizar o README
- Gera a animação de "snake" baseada nas contribuições
- Faz push de ambos para a branch `output`

### 4. Sistema de Cache e Logs

- **cache_manager.py**: Gerencia o cache para reduzir chamadas à API
- **logger.py**: Configura logs para diagnósticos

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

## Boas Práticas

### .gitignore

O arquivo `.gitignore` está configurado para ignorar:

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
