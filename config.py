import os

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key')
    DEBUG = os.getenv('FLASK_DEBUG', True)
    
    # API keys for external services
    UNIPROT_API_KEY = os.getenv('UNIPROT_API_KEY', '')
    PDB_API_KEY = os.getenv('PDB_API_KEY', '')
    DRUGBANK_API_KEY = os.getenv('DRUGBANK_API_KEY', '')
    CHEMBL_API_KEY = os.getenv('CHEMBL_API_KEY', '')
    
    # Cache settings
    CACHE_EXPIRY = 3600  # 1 hour