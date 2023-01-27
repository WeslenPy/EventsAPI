from app.routers import *
from app.server.instance import app as application

app = application.app

if __name__ == '__main__':
    application.run()