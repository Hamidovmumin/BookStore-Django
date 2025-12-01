from django.urls import path
from . import views

urlpatterns = [
    path('writer/<int:id>/', views.get_writer, name='writer'),
    path('book_detail/<int:id>/', views.book_detail, name='book_detail'),
    path('delete_comment/<int:id>/', views.delete_comment, name='delete_comment'),
]