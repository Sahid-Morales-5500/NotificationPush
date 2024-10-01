from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Proyecto import settings
from .models import PushSuscription
from webpush import send_user_notification
import json


def get_public_key(request):
    vapid_public_key = settings.VAPID_PUBLIC_KEY
    return JsonResponse({'VapidPublicKey': vapid_public_key})

@csrf_exempt
def save_push_subscription(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        subscription = PushSuscription(
            endpoint=data['endpoint'],
            keys_auth=data['keys']['auth'],
            keys_p256dh=data['keys']['p256dh']
        )
        subscription.save()
        return JsonResponse({'status': 'subscription saved'})
    else:
        return JsonResponse({'status': 'invalid request'}, status=400)
        


@csrf_exempt
def send_push_notification(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Obtener el endpoint del usuario a través del ID del usuario o algún identificador
        user_id = data.get('user_id')
        try:
            subscription = PushSuscription.objects.get(id=user_id)
        except PushSuscription.DoesNotExist:
            return JsonResponse({"error": "Usuario no suscrito"}, status=404)
        
        # Construir el payload (los datos que se enviarán en la notificación)
        payload = {
            "title": data.get('title', 'Notificación'),
            "body": data.get('body', 'Este es el cuerpo de la notificación'),
            "icon": data.get('icon', 'https://example.com/icon.png')  # Puedes cambiar el icono aquí
        }

        # Enviar la notificación utilizando django-webpush y pywebpush
        try:
            send_user_notification(
                subscription_info={
                    "endpoint": subscription.endpoint,
                    "keys": {
                        "p256dh": subscription.keys_p256dh,
                        "auth": subscription.keys_auth
                    }
                },
                payload=json.dumps(payload),
                ttl=1000  # Time to Live (TTL)
            )
            return JsonResponse({"status": "Notificación enviada con éxito"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método no soportado"}, status=405)