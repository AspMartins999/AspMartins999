import requests
import random
import re
import feedparser
import datetime
import sys
import os

# Adicionar o diretório atual ao path para importar os módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.cache_manager import get_cached_data, set_cached_data
    from utils.logger import setup_logger
except ImportError:
    # Criar os diretórios necessários se não existirem
    os.makedirs('utils', exist_ok=True)
    print("Módulos de utilidades não encontrados. Execute o script novamente após a criação dos módulos.")
    sys.exit(1)

# Configuração do logger
logger = setup_logger("update_readme")

# Constantes
USERNAME = "AspMartins999"
README_PATH = "README.md"
BLOG_RSS = "https://matheusmartins.dev.br/rss.xml"  # atualizar quando o blog estiver pronto
MAX_PRS = 5
MAX_POSTS = 3
QUOTES = [
    "A simplicidade é a alma da eficiência. — Austin Freeman",
    "Primeiro, resolva o problema. Depois, escreva o código. — John Johnson",
    "Andar sobre a água e desenvolver software a partir de especificações são fáceis se ambos estiverem congelados. — Edward V. Berard",
    "Qualquer tolo pode escrever código que um computador entenda. Bons programadores escrevem código que humanos entendam. — Martin Fowler",
    "Em caso de incêndio: git commit, git push, saia do prédio.",
    "Software é como entropia: É difícil de compreender, não pesa nada e obedece à segunda lei da termodinâmica; ou seja, sempre aumenta. — Norman Augustine",
    "A melhor maneira de prever o futuro é implementá-lo. — Alan Kay",
    "Todo grande desenvolvedor que você conhece chegou lá resolvendo problemas para os quais não estava qualificado até realmente fazê-lo. — Patrick McKenzie"
]

def get_merged_prs(user: str):
    """
    Busca os PRs mesclados do usuário via API do GitHub com cache e tratamento de erros.
    
    Args:
        user (str): Nome do usuário no GitHub
        
    Returns:
        tuple: (total de PRs, markdown formatado com os PRs)
    """
    cache_key = f"merged_prs_{user}"
    cached_data = get_cached_data(cache_key)
    
    if cached_data:
        logger.info(f"Usando PRs em cache para o usuário {user}")
        return cached_data
        
    try:
        url = f"https://api.github.com/search/issues?q=is:pr+author:{user}+is:merged"
        logger.info(f"Buscando PRs mesclados para {user}")
        
        headers = {}
        # Usar token do GitHub se disponível para aumentar o limite de requisições
        if 'GITHUB_TOKEN' in os.environ:
            headers['Authorization'] = f"token {os.environ['GITHUB_TOKEN']}"
            
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        
        data = r.json()
        total = data.get("total_count", 0)
        logger.info(f"Encontrados {total} PRs mesclados para {user}")
        
        prs = []
        emojis = ["🥳", "🎉", "🎊", "🥂", "🙌🏼"]
        
        for i, item in enumerate(data.get("items", [])[:MAX_PRS]):
            emoji = emojis[i % len(emojis)]
            pr_url = item["html_url"]
            repo_url = re.sub(r'/pull/\d+', '', pr_url)
            prs.append(f"{i+1}. {emoji} Merged PR [{item['number']}]({pr_url}) - [{item['repository_url'][29:]}]({repo_url})")
        
        result = (total, "\n".join(prs))
        # Salvar no cache
        set_cached_data(cache_key, result)
        return result
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao buscar PRs: {str(e)}")
        return 0, f"*Erro ao buscar PRs: {str(e)}*"
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar PRs: {str(e)}")
        return 0, "*Erro inesperado ao buscar PRs*"

def get_latest_posts(rss_url: str, max_items: int = 3):
    """
    Busca os posts mais recentes do blog via feed RSS com cache e tratamento de erros.
    
    Args:
        rss_url (str): URL do feed RSS
        max_items (int): Número máximo de posts para exibir
        
    Returns:
        str: Markdown formatado com os posts mais recentes
    """
    cache_key = f"blog_posts_{rss_url}"
    cached_data = get_cached_data(cache_key)
    
    if cached_data:
        logger.info("Usando posts do blog em cache")
        return cached_data
    
    try:
        logger.info(f"Buscando posts recentes do feed: {rss_url}")
        feed = feedparser.parse(rss_url)
        
        # Verificar se o feed está disponível e tem entradas
        if hasattr(feed, 'status') and feed.status != 200:
            logger.warning(f"Feed RSS retornou status {feed.status}")
            return "*Feed do blog não disponível no momento*"
            
        if not feed.entries:
            logger.info("Feed RSS não tem entradas")
            return "*Nenhum post de blog encontrado*"
        
        posts = []
        for e in feed.entries[:max_items]:
            try:
                date = datetime.datetime(*e.published_parsed[:6]).strftime('%Y-%m-%d') if getattr(e, 'published_parsed', None) else ""
                posts.append(f"- [{e.title}]({e.link}) — {date}")
            except (AttributeError, TypeError) as err:
                logger.warning(f"Erro ao processar entrada do feed: {err}")
                continue
        
        result = "\n".join(posts)
        # Salvar no cache
        set_cached_data(cache_key, result)
        return result
        
    except Exception as e:
        logger.error(f"Erro ao buscar posts do blog: {str(e)}")
        return "*Erro ao buscar posts do blog. Tente novamente mais tarde.*"

def replace_block(text: str, start: str, end: str, replacement: str):
    """
    Substitui o conteúdo entre marcadores de início e fim em um texto.
    
    Args:
        text (str): Texto completo
        start (str): Marcador de início
        end (str): Marcador de fim
        replacement (str): Texto substituto
        
    Returns:
        str: Texto com a substituição feita
    """
    pattern = rf'({re.escape(start)}\n)(.*?)(\n{re.escape(end)})'
    return re.sub(pattern, rf'\1{replacement}\3', text, flags=re.DOTALL)

def backup_readme():
    """Cria um backup do README antes de modificá-lo."""
    try:
        from datetime import datetime
        backup_dir = ".backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"README_{timestamp}.md")
        
        if os.path.exists(README_PATH):
            with open(README_PATH, "r", encoding="utf-8") as src:
                with open(backup_file, "w", encoding="utf-8") as dst:
                    dst.write(src.read())
            logger.info(f"Backup do README criado: {backup_file}")
        return True
    except Exception as e:
        logger.error(f"Erro ao criar backup do README: {str(e)}")
        return False

def update_readme():
    """Função principal que atualiza o README com informações dinâmicas."""
    try:
        logger.info("Iniciando atualização do README")
        
        # Criar backup antes de modificar
        backup_readme()
        
        # Buscar dados para as seções dinâmicas
        total_prs, prs_md = get_merged_prs(USERNAME)
        prs_count_badge = f'<span><img src="https://img.shields.io/badge/Total_Merged_PRs-{total_prs}-1877F2?style=for-the-badge"></span>'
        
        blog_md = get_latest_posts(BLOG_RSS, MAX_POSTS)
        quote = random.choice(QUOTES)
        
        # Verificar se o README existe
        if not os.path.exists(README_PATH):
            logger.error(f"README não encontrado em {README_PATH}")
            return False
        
        # Ler o conteúdo atual
        with open(README_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Fazer as substituições
        content = replace_block(content, "<!--Start Count Merged PRs-->", "<!--Finish Count Merged PRs-->", prs_count_badge)
        content = replace_block(content, "<!--Start Merged PRs-->", "<!--Finish Merged PRs-->", prs_md)
        
        # Substituir a seção de blog apenas se houver conteúdo
        if blog_md:
            content = replace_block(content, "<!--START_SECTION:blog-->", "<!--END_SECTION:blog-->", blog_md)
        
        content = replace_block(content, "<!--START_QUOTE-->", "<!--END_QUOTE-->", quote)
        
        # Escrever o conteúdo atualizado
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(content)
            
        logger.info("README atualizado com sucesso")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao atualizar README: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        update_readme()
        logger.info("Script executado com sucesso")
    except Exception as e:
        logger.error(f"Erro na execução do script: {str(e)}")
        sys.exit(1)
