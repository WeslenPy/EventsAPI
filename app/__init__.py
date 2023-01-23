
from .databases.events.models import *
from .routers.v1 import *

from .server.instance import app

app = app.app