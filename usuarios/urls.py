from django.urls import path
from . import views

from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/home/', permanent=False)),
    path('home/', views.home, name='home'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('materiais/', views.todos_materiais, name='todos_materiais'),
    path('avisos/', views.todos_avisos, name='todos_avisos'),
]