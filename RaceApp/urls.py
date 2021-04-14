
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('logout', views.logout),
    path('register', views.register),
    path('main', views.main),
    path('stats/<int:id>', views.stats),
    path('edit', views.edit),
    path('race', views.race),
    path('runs', views.runs),
    path('messageboard', views.messageboard),
    path('add_run', views.add_run),
    # path('add_message', views.add_message),
    # path('add_comment', views.add_comment),
    # path('delete_message', views.delete_message),
    # path('delete_comment', views.delete_comment),
    path('edit/<int:id>', views.edit),
    # path('user/<int:id>', views.user),
]
