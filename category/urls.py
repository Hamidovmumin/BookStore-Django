from django.urls import path
from . import views

urlpatterns = [
    path('category/<slug:slug>/', views.get_category, name='category'),
]