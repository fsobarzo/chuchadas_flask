#############################################################
# - Template para las configuraciones
# - Cambiar el nombre a config.py
# - Agregar configuraciones de flask aca
# - Para utilizar estas configuraciones
#
# import config.py
# 
# config.CONFIG_NAME
#############################################################

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
#THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = 'mysecretkey'

#ALLOWED_EXTENSIONS = set(['jpeg','png','jpg','gif'])
# Define the database - we are working with
# SQLite for this example
#SQLite
#DATABASE_URI = 'sqlite:////absolute/path/to/foo.db'
#POSTGRES
#DATABASE_URI = 'postgresql://scott:tiger@localhost/mydatabase'
#MySQL
SQLALCHEMY_DATABASE_URI = 'mysql://chuchas_user:chuchas@localhost/chuchas'
#DATABASE_CONNECT_OPTIONS = {}
