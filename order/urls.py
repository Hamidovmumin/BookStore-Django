from django.urls import path
from .views import order,load_districts,OrderPDFView

urlpatterns = [
    path('', order, name='order'),
    path('load-ajax_load_districts/', load_districts, name='ajax_load_districts'),
    path('pdf/<int:id>', OrderPDFView.as_view(), name='order_pdf'),
]