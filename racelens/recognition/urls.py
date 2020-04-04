from django.urls import path, include

from . import views


app_name = "recognition"

urlpatterns = [
    path('', views.index, name="index"),
    path('eventos/', include([
        path('', views.list_events, name="events"),
        path('create', views.create_event, name="create_event"),
        path('<slug:slug>', views.uploadSelfie, name="get_event"),
        path('<slug:slug>/upload', views.uploadPhoto, name="upload_event"),
    ])),
    path('contacto/', views.contact, name="contact"),
    path('politica-de-privacidad/', views.politica_de_privacidad, name="privacy-policy")
]