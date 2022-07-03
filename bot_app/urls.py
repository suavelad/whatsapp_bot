import django


from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import whatsapp_message_bot,whatsapp_message_image, whatsapp_message_status

router = DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    # path('messages/',whatsapp_message_bot,name='whatsapp_message_bot'),
    path('messages/',whatsapp_message_image,name='whatsapp_message_bot'),
    path('status/',whatsapp_message_status,name='whatsapp_message_status'),
    
]


