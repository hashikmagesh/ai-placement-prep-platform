from django.urls import path
from . import views

app_name='prep'

urlpatterns = [
    path('',views.home_page,name='home'),
    path('roadmap',views.roadmap_view,name='roadmap'),
    path("my_roadmaps/", views.my_roadmaps, name="my_roadmaps"),
    path("roadmap/<int:roadmap_id>/", views.roadmap_detail, name="roadmap_detail"),
    path("roadmap/<int:roadmap_id>/delete/", views.delete_roadmap, name="delete_roadmap"),
    path('roadmap_history_generate',views.roadmap_history_generate,name='roadmap_history_generate'),


    path('practice',views.practice,name='practice'),
    path('ask_ai',views.ask_ai,name='ask_ai'),
    path("practice/aptitude/", views.aptitude_view, name="aptitude"),
    path("practice/coding/", views.coding_view, name="coding"),
    path("practice/interview/", views.interview_view, name="interview"),

    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('reset_password/<uidb64>/<token>',views.reset_password,name='reset_password'),

    path("ai-chat/", views.ai_chat_view, name="ai_chat"),

    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('dashboard/', views.progress_dashboard, name='dashboard'),

    path("resume_analyzer/", views.resume_analyzer, name="resume_analyzer"),
    
]
