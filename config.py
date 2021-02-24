import os

class CONFIG:
    def __init__(self):
        #
        # Basic Server Settings
        #
        self.ENV = os.environ.get("ENVIRONMENT")
        self.DEBUG = True if self.ENV == 'dev' else False
        self.SERVER_HOST = '127.0.0.1'
        self.SERVER_PORT = 8000
        if self.ENV == 'dev':
            self.HOST_BASE_URL = f'http://{self.SERVER_HOST}:{self.SERVER_PORT}'
            self.CLIENT_BASE_URL = 'http://localhost:3000'
        elif self.ENV == 'staging':
            self.HOST_BASE_URL = 'https://api.yardsalemanager.meqsoftware.com'
            self.CLIENT_BASE_URL = 'https://yardsalemanager.meqsoftware.com'
        elif self.ENV == 'prod':
            self.HOST_BASE_URL =  os.environ.get('HOST_BASE_URL') # 'https://api.yardsalemanager.com'
            self.CLIENT_BASE_URL = os.environ.get('CLIENT_BASE_URL') # 'https://yardsalemanager.com'
        #
        # CORS Allowed Origins
        #
        self.CLIENT_ORIGINS = self.CLIENT_BASE_URL
        self.SECRET_KEY = os.environ.get('SECRET_KEY') 
        #
        # Send Grid Credentials/Settings
        #
        self.SEND_GRID_API_KEY = os.environ.get('SEND_GRID_API_KEY') 
        self.SEND_GRID_FROM_EMAIL = os.environ.get('SEND_GRID_API_KEY')
        self.SEND_GRID_TO_EMAIL = os.environ.get('SEND_GRID_API_KEY')
        #
        # Security/Password
        #
        self.BCRYPT_SALT = os.environ.get('BCRYPT_SALT').encode('utf-8') 
        #
        # Folders
        #
        self.UPLOAD_FOLDER = 'generated_files'
        #
        # GraphQL Server
        #
        self.GRAPHQL_ENDPOINT = os.environ.get("GRAPHQL_ENDPOINT")
        self.GRAPHQL_ADMIN_SECRET = os.environ.get("GRAPHQL_ADMIN_SECRET")
        #
        # Load JWT Private Key File if dev else load from .env
        #
        if self.ENV == 'dev':
            with open('instance/jwt-key', 'r') as jwt_key:
                # print('\n\n\n\n\nJWT SECRET: ', jwt_secret.read())
                self.JWT_SECRET = jwt_key.read()
        else:
            self.JWT_SECRET = os.environ.get("JWT_SECRET")
        #
        # Load JWT Public Key File if dev else load from .env
        #
        if self.ENV == 'dev':
            with open('instance/jwt-key.pub', 'r') as jwt_pub_key:
                # print('\n\n\n\n\nJWT SECRET: ', jwt_secret.read())
                self.JWT_PUBLIC_KEY = jwt_pub_key.read()
        else:
            self.JWT_PUBLIC_KEY = os.environ.get("JWT_PUBLIC_KEY")
        
        self.ACCESS_TOKEN_EXPIRE = 60 * 2  # in seconds
        self.REFRESH_TOKEN_EXPIRE = 1 * \
            (24 * 60 * 60)  # days expressed in seconds
        self.JWT_AUDIENCE = self.HOST_BASE_URL
