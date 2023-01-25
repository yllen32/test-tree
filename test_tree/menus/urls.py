from django.urls import path

from .views import menu

urlpatterns = [
    path('menu/<str:slug>', view=menu, name='menu')
]
