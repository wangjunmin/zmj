from django.urls import path, include
import django_eventstream
from . import views
app_name = 'modbus'
urlpatterns = [
    path('', views.home),
    path('show_data/', views.show_it, name='show'),
    path('events/', include(django_eventstream.urls), {
        'channels': ['time', 'monitor']
    }),
    path("imp_excel/", views.imp_excel, name='imp_excel'),
    path("show_monitor/", views.show_monitor, name='show_monitor'),
]
