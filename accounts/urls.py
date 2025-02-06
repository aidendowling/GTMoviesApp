from django.urls import path
from . import views
urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('orders/', views.orders, name='accounts.orders'),
]