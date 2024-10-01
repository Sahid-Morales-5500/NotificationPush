from django.urls import path
from .views import get_public_key,save_push_subscription,send_push_notification

urlpatterns = [
    path('get-public-vapid', get_public_key, name='get_public_key'),
    path('subscribe-notifications',save_push_subscription, name='save_push_suscription' ),
    path('send-notification', send_push_notification, name='send-notification'),
    path('send-notification', send_push_notification, name='send-notification'),
]