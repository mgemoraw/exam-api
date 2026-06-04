"""
"""
from pathlib import Path 
"""Frontend module for Avery Production"""
from .router import router, templates, setup_frontend

__all__ = ["router", "templates", "setup_frontend"]

BASE_DIR = Path(__file__).parent

TEMPLATE_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'


