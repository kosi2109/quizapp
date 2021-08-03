from django.urls import path
from .views import *
app_name = 'questions' 

urlpatterns = [
	path('register/', registerPage , name='registerPage'),
	path('userLogout/', userLogout , name='userLogout'),
	path('login/', userLogin , name='userLogin'),
	path('', home , name='home'),
	path('createQuiz/', createQuiz , name='createQuiz'),
	path('group/<slug:slug>', group , name='group'),
	path('score/<slug:slug>', score , name='score'),
	path('ctView/<slug:slug>', ctView , name='ctView'),

	path('edit/<slug:slug>', edit , name='edit'),
	path('deletegroup/<slug:slug>', deletegroup , name='deletegroup'),
	path('editQuestion/<slug:slug>', editQuestion , name='editq'),
	path('deletequestion/<slug:slug>', deletequestion , name='deletequestion'),
	path('reanswer/', reanswer , name='reanswer'),
	path('myquizView/', myquizView , name='myquizView'),
]