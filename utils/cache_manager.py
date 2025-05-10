import os
import json
import time
import logging
from datetime import datetime, timedelta

CACHE_DIR = ".cache"
CACHE_FILE = os.path.join(CACHE_DIR, "github_cache.json")
CACHE_EXPIRY = 3600  # 1 hora em segundos

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("update_readme.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("cache_manager")

def ensure_cache_dir():
    """Garante que o diretório de cache existe."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
        logger.info(f"Diretório de cache criado: {CACHE_DIR}")

def load_cache():
    """Carrega dados do cache."""
    ensure_cache_dir()
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                logger.debug("Cache carregado com sucesso")
                return cache_data
    except Exception as e:
        logger.error(f"Erro ao carregar cache: {e}")
    return {}

def save_cache(cache_data):
    """Salva dados para o cache."""
    ensure_cache_dir()
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
            logger.debug("Cache salvo com sucesso")
    except Exception as e:
        logger.error(f"Erro ao salvar cache: {e}")

def get_cached_data(key):
    """Obtém dados do cache se ainda forem válidos."""
    cache = load_cache()
    if key in cache:
        timestamp = cache[key].get("timestamp", 0)
        if time.time() - timestamp < CACHE_EXPIRY:
            logger.info(f"Usando dados em cache para: {key}")
            return cache[key].get("data")
    return None

def set_cached_data(key, data):
    """Armazena dados no cache com timestamp."""
    cache = load_cache()
    cache[key] = {
        "data": data,
        "timestamp": time.time()
    }
    save_cache(cache)
    logger.info(f"Dados armazenados em cache para: {key}")
