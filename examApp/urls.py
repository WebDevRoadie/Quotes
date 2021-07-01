from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('post_quote', views.post_quote),
    path('posted_by/<int:id>', views.posted_by),
    path('account/<int:id>', views.account),
    path('delete/<int:id>', views.delete),
    path('edit/<int:id>', views.edit),
    path('like/<int:id>', views.like),
]