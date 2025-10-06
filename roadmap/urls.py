from django.urls import path
from . import views

urlpatterns = [
    path('select/', views.select_page, name='select'),
    path('roadmap/', views.roadmap_page, name='roadmap'),
    path('reset/', views.reset_progress, name='reset'),
]