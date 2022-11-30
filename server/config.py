import os
from credentials import client_id_local, client_secret_local

class ProductionConfig():
    DEBUG = False
    DEVELOPMENT = False
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")


class DevelopmentConfig():
    DEBUG = True
    DEVELOPMENT = False
    CLIENT_ID = client_id_local
    CLIENT_SECRET = client_secret_local