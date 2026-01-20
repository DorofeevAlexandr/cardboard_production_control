from django.urls import path, re_path, register_converter
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('tuning', views.tuning, name='tuning'),
    path('open_pdf_file_view/<path:filename>/', views.open_pdf_file_view, name='open_pdf_file_view'),
]
