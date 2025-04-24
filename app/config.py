"""
Configuration settings for the CPU Scheduler Simulation web application.
"""

import os
from datetime import timedelta

class Config:
    """Base configuration."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-development-only')

    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'app/uploads')
    OUTPUT_FOLDER = os.environ.get('OUTPUT_FOLDER', 'app/static/output')
    ALLOWED_EXTENSIONS = {'csv', 'json'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  
    
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SESSION_TYPE = 'filesystem'
    
    DEFAULT_ALGORITHM = 'all'
    DEFAULT_PROCESS_COUNT = 5
    DEFAULT_MIN_BURST = 1
    DEFAULT_MAX_BURST = 10
    DEFAULT_MIN_ARRIVAL = 0
    DEFAULT_MAX_ARRIVAL = 10
    DEFAULT_MIN_PRIORITY = 1
    DEFAULT_MAX_PRIORITY = 10
    DEFAULT_QUANTUM = 2

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    
class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get('SECRET_KEY')

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}