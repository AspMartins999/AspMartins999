import logging

def setup_logger(name, log_file="update_readme.log"):
    """
    Configura e retorna um logger personalizado.
    
    Args:
        name (str): Nome do logger
        log_file (str): Arquivo de log
        
    Returns:
        Logger: Objeto logger configurado
    """
    logger = logging.getLogger(name)
    
    # Configura o logger se ele ainda não estiver configurado
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Handler para arquivo
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        )
        
        # Adiciona os handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger
