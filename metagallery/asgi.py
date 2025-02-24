"""
ASGI config for metagallery project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os


from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metagallery.settings')

django_asgi_app = get_asgi_application()
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.middleware import JWTAuthMiddleWare
import chat.routing


# application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleWare(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    )
})