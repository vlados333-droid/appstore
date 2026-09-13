from django.urls import path, register_converter

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.category_detail, name='category'),

    path('about/', views.AboutView.as_view(), name='about'),
    path('app/<int:app_id>/', views.AppDetailView.as_view(), name='app_detail'),
    path('new/', views.NewAppView.as_view(), name='new'),

    path('free-apps/', views.AppsIsFreeListView.as_view(), {'is_free': True}, name='free_apps'),
    path('paid-apps/', views.AppsIsFreeListView.as_view(), {'is_free': False}, name='paid_apps'),

    path('api/app/<int:app_id>/', views.api_app_detail, name='api_app_detail'),
]
