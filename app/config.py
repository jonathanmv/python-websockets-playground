import os


class Config:
    WEBSOCKET_URI = "wss://fstream.binance.com/ws/ethusdt@bookTicker"
    PCAP_FILE = "capture.pcap"
    SSL_KEYLOG_FILE = os.getenv('SSLKEYLOGFILE')

    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    WEBSOCKET_URI = "wss://fstream.binance.com/ws/ethusdt@bookTicker"


# Dictionary to map environment names to configuration classes
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}


def get_config(env_name) -> Config:
    return config_by_name.get(env_name, Config)
