
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('fav_questions/', views.fav_questions, name='fav_questions'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('fav_profiles/', views.fav_profiles, name='fav_profiles'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('question_follow/<int:pk>', views.question_follow, name="question_follow"),
    path('question_info/<int:pk>', views.question_info, name="question_info"),
    path('question_delete/<int:pk>', views.question_delete, name="question_delete"),
    path('answer_like/<int:pk>', views.answer_like, name="answer_like"),
    path('answer_delete/<int:pk>', views.answer_delete, name="answer_delete"),
]
