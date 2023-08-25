from django.urls import path
from accounts.socket_authentication import TokenAuthMiddleware
from accounts.consumers import NotificationConsumer

from accounts.views import LoginView, TriggerNotification

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('trigger_notifications/', TriggerNotification.as_view()),
    
]

websocket_urls = [
    path("ws/notification/", TokenAuthMiddleware(NotificationConsumer.as_asgi())),
    
]