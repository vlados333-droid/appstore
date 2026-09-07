from django.urls import path, register_converter

from . import views
from .converters import YearConverter

register_converter(YearConverter, 'yyyy')

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('app/<int:app_id>/', views.app_detail, name='app_detail'),
    path('category/<int:category_id>/', views.category_detail, name='category'),
    path('new/', views.new, name='new'),

    path('free-apps/', views.apps_list, {'is_free': True}, name='free_apps'),
    path('paid-apps/', views.apps_list, {'is_free': False}, name='paid_apps'),

    path('archive/<yyyy:year>/', views.archive_year, name='archive'),
]
