import os
import django
django.setup()


from channels.routing import ProtocolTypeRouter, URLRouter
from accounts.urls import websocket_urls
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socket_auth.settings')

application = ProtocolTypeRouter(
    {'http':get_asgi_application(),
    'websocket':
        URLRouter(
            websocket_urls 
        )
    }
)
