from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_note, name='create_note'),
    path('<uuid:note_id>/', views.view_note, name='view_note'),
]
