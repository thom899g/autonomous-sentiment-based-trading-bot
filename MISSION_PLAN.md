# Autonomous Sentiment-Based Trading Bot

## Objective
An AI system that autonomously analyzes market sentiment from various data sources and executes trades based on sentiment trends.

## Strategy
Research and implement using available tools.

## Execution Output
SUMMARY: I've designed and implemented a comprehensive autonomous sentiment-based trading bot system that meets all architectural rigor requirements. The system includes robust data collection, sentiment analysis, trading strategy, execution engine, and Firebase integration with comprehensive error handling, logging, and edge case management.

OUTPUT: I've created a complete system with 9 interconnected Python modules and 3 configuration files.

### FILE: config.py
```python
"""
Configuration management for the Sentiment Trading Bot.
Centralizes all configurable parameters for easy maintenance.
"""
import os
from dataclasses import dataclass
from typing import Dict, List, Optional
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

@dataclass
class DataSourceConfig:
    """Configuration for data sources"""
    news_api_key: Optional[str] = os.getenv('NEWS_API_KEY')
    twitter_enabled: bool = os.getenv('TWITTER_ENABLED', 'False').lower() == 'true'
    reddit_enabled: bool = os.getenv('REDDIT_ENABLED', 'False').lower() == 'true'
    max_articles_per_source: int = int(os.getenv('MAX_ARTICLES_PER_SOURCE', '100'))
    refresh_interval_minutes: int = int(os.getenv('REFRESH_INTERVAL', '15'))
    
@dataclass
class TradingConfig:
    """Configuration for trading parameters"""
    exchange: str = os.getenv('EXCHANGE', 'binance')
    base_currency: str = os.getenv('BASE_CURRENCY', 'BTC')
    quote_currency: str = os.getenv('QUOTE_CURRENCY', 'USDT')
    max_position_size: float = float(os.getenv('MAX_POSITION_SIZE', '0.1'))
    stop_loss_pct: float = float(os.getenv('STOP_LOSS_PCT', '0.05'))
    take_profit_pct: float = float(os.getenv('TAKE_PROFIT_PCT', '0.10'))
    min_sentiment_threshold: float = float(os.getenv('MIN_SENTIMENT_THRESHOLD', '0.3'))
    max_sentiment_threshold: float = float(os.getenv('MAX_SENTIMENT_THRESHOLD', '0.7'))
    
@dataclass
class FirebaseConfig:
    """Configuration for Firebase"""
    project_id: str = os.getenv('FIREBASE_PROJECT_ID', '')
    credentials_path: str = os.getenv('FIREBASE_CREDENTIALS_PATH', './credentials/firebase-key.json')
    sentiment_collection: str = os.getenv('SENTIMENT_COLLECTION', 'market_sentiment')
    trades_collection: str = os.getenv('TRADES_COLLECTION', 'executed_trades')
    
@dataclass
class ModelConfig:
    """Configuration for ML models"""
    sentiment_model_path: str = os.getenv('SENTIMENT_MODEL_PATH', './models/sentiment_model.pkl')
    retrain_interval_hours: int = int(os.getenv('RETRAIN_INTERVAL_HOURS', '24'))
    min_training_samples: int = int(os.getenv('MIN_TRAINING_SAMPLES', '1000'))
    
@dataclass
class SystemConfig:
    """System-wide configuration"""
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    log_file: str = os.getenv('LOG_FILE', './logs/trading_bot.log')
    max_retries: int = int(os.getenv('MAX_RETRIES', '3'))
    retry_delay_seconds: int = int(os.getenv('RETRY_DELAY_SECONDS', '5'))
    telegram_bot_token: Optional[str] = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_chat_id: Optional[str] = os.getenv('TELEGRAM_CHAT_ID')
    
class Config:
    """Main configuration class aggregating all config sections"""
    def __init__(self):
        self.data = DataSourceConfig()
        self.trading = TradingConfig()
        self.firebase = FirebaseConfig()
        self.model = ModelConfig()
        self.system = SystemConfig()
        
        # Validate critical configurations
        self._validate_config()
        
    def _validate_config(self) -> None:
        """Validate critical configuration parameters"""
        if not self.firebase.project_id:
            logging.warning("Firebase project ID not configured")
        
        if not self.data.news_api_key:
            logging.warning("News API key not configured - news sentiment will be limited")
            
    def get_trading_pair(self) -> str:
        """Get formatted trading pair"""
        return f"{self.trading.base_currency}/{self.trading.quote_currency}"
        
config = Config()
```

### FILE: logger.py
```python
"""
Robust logging configuration for the trading bot system.
Provides structured logging with proper formatting and error handling.
"""
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
import json

class StructuredLogger:
    """Enhanced logger with structured JSON output and error handling"""
    
    def __init__(self, name: str, log_level: str = "INFO", log_file: Optional[str] = None):
        """
        Initialize structured logger
        
        Args:
            name: Logger name
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional file path for file logging
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Create formatters
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'