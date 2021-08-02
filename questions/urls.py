from django.urls import path
from .views import *
app_name = 'questions' 

urlpatterns = [
	path('login/', userLogin , name='userLogin'),
	path('', home , name='home'),
	path('createQuiz/', createQuiz , name='createQuiz'),
	path('group/<slug:slug>', group , name='group'),
	path('score/<slug:slug>', score , name='score'),
	path('ctView/<slug:slug>', ctView , name='ctView'),

	path('reanswer/', reanswer , name='reanswer'),
]