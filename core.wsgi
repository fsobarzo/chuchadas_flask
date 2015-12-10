import sys
import os

PROYECT = "chuchadas"
PATH = "/home/%s/backend/" % PROYECT
sys.path.insert(0,PATH)

from app import app as application
