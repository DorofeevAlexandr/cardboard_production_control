from django.urls import path, re_path, register_converter
from . import views
from .views import MyPDFView

urlpatterns = [
    path('', views.index, name='home'),
    path('tuning', views.tuning, name='tuning'),
    path('pdf-file/', MyPDFView.as_view(response_type='pdf'), name='pdf-file'),
    path('pdf-html/', MyPDFView.as_view(response_type='html'), name='pdf-html'),
    path('pdf-download/', MyPDFView.as_view(response_type='download'), name='pdf-download'),
]
