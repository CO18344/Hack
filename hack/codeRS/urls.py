from django.urls import path, re_path

from . import views
'''
Naming your URL lets you refer to it unambiguously 
from elsewhere in Django, especially from within templates.
'''
urlpatterns = [
    path('sign/', views.sign, name='sign'),
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_, name='login'),
    path('dashboard/', views.dashboard, name='dash'),
    path('dashboard/problems/', views.problems, name='problem'),
    path('dashboard/problems/code/', views.code, name='code'),
    path('dashboard/problems/code/update/', views.update, name='update'),
    path('pending/', views.pending, name='pending'),
    path('download/', views.download_csv, name='download'),

    # this is just for testing purpose
    path('test/', views.test, name='test'),
]