from django.urls import path, re_path, register_converter
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('electricity_meter_day', views.electro_counters_statistics_for_the_day,
         name='electro_counters_statistics_for_the_day'),
    path('electricity_meter_month', views.electro_counters_statistics_for_the_day,
         name='electro_counters_statistics_for_the_month'),
    path('tuning', views.tuning, name='tuning'),
    path('open_pdf_file_view/<path:filename>/', views.open_pdf_file_view, name='open_pdf_file_view'),
]
