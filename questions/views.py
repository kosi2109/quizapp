from django.shortcuts import render,redirect
from .models import * 
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .decorator import unauthenticated_user


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','email','password1','password2']
		widgets = {
			'username': forms.TextInput(attrs={'id':'username','placeholder':'Username'}),
			'email': forms.TextInput(attrs={'id':'exampleInputEmail1','placeholder':'Email'}),
			'password1': forms.PasswordInput(attrs={'id':'Password1'}),
			'password2': forms.PasswordInput(attrs={'id':'Password2'}),
		}

@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('username')
			Answerer.objects.create(
				user = user ,
				email = email,
				name=username
				)
			messages.success(request, 'Account has been created for' + username)
			return redirect('questions:userLogin')


	ctx = {'form':form}
	return render(request,'signup.html',ctx)

@unauthenticated_user
def userLogin(request):
	if request.method == 'POST' or None:
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('questions:home')
		else:
			messages.info(request,'Username or Password is incorrect..')
			return redirect('questions:userLogin')

	return render(request ,'login.html' )


def userLogout(request):
	logout(request)
	return redirect('questions:userLogin')

@login_required(login_url='questions:userLogin')
def home(request):
	gp = QuestionGp.objects.all()
	ct = Category.objects.all()
			
	ctx = {'gp':gp,'ct':ct}
	return render(request, 'index.html',ctx)


@login_required(login_url='questions:userLogin')
def group(request,slug):
	gp = QuestionGp.objects.get(gp_slug=slug)
	questions = gp.question_set.all()
	user = request.user.answerer

	
	if UserGpPoint.objects.filter(answerer=user,gp=gp):
		gpansed = UserGpPoint.objects.get(answerer=user,gp=gp)
		useranss = gpansed.useranswer_set.all()
		correctans = {}
		userans = {}
		# I dont want to stat from index 0
		coQ = 1
		coA = 1
		for i in questions:
			correctans[coQ] = i.answer
			coQ += 1
		for i in useranss:
			userans[coA] = i.answer
			coA += 1
		score = gpansed.point
		ctx={'questions':questions,'score':score,'correctans':correctans ,'userans':userans,'gp':gp,'gpansed':gpansed}
		return render(request, 'group.html',ctx)
		

	else:
		if request.method == "POST":
			usergp = UserGpPoint.objects.create(answerer=user,gp=gp)
			getusergp = UserGpPoint.objects.get(answerer=user,gp=gp)
			scoreurl = getusergp.slug
			cont = 0
			for i in questions:
				qans = i.answer
				cont += 1
				ans = request.POST.get('ans['+str(cont)+']')
				print(ans)
				UserAnswer.objects.create(point=usergp,question=i,answer=ans)
				if int(qans) == int(ans):
					usergp.point += 1
					usergp.save()
					
			return redirect('http://quizdemo-bykosi.herokuapp.com/score/'+scoreurl)

	ctx={'questions':questions,'gp':gp}
	return render(request, 'group.html',ctx)
	



@login_required(login_url='questions:userLogin')
def ctView(request,slug):
	cct = Category.objects.get(ct_slug=slug)
	gp = QuestionGp.objects.filter(category=cct)
	ct = Category.objects.all()
	ctx = {'gp':gp,'ct':ct,'cct':cct}
	return render(request, 'ctview.html',ctx)


@login_required(login_url='questions:userLogin')
def myquizView(request):
	user = request.user.answerer
	gp = QuestionGp.objects.filter(created_by=user)
	ct = Category.objects.all()
	ctx = {'gp':gp,'ct':ct}
	return render(request, 'myquiz.html',ctx)



@login_required(login_url='questions:userLogin')
def score(request,slug):
	user = request.user.answerer
	gp = UserGpPoint.objects.get(answerer=user,slug=slug)
	ans = gp.useranswer_set.all()
	total = len(ans)

	ctx={'gp':gp,'total':total}
	return render(request, 'score.html',ctx)



@login_required(login_url='questions:userLogin')
def createQuiz(request):
	ct = Category.objects.all()
	user = request.user.answerer
	if request.method == 'POST':
		cate = request.POST.get('category')
		gp_name = request.POST.get('gp_name')
		
		counter = request.POST.get('counter')

		category = Category.objects.get(id=cate) 
		gp = QuestionGp.objects.create(
			created_by=user,
			category=category,
			gp_name=gp_name,
			)

		for i in range(int(counter)+1):
			question = request.POST.get('question'+str(i))
			answer = request.POST.get('answer'+str(i))
			ans1 = request.POST.get('ans1'+str(i))
			ans2 = request.POST.get('ans2'+str(i))
			ans3 = request.POST.get('ans3'+str(i))
			ans4 = request.POST.get('ans4'+str(i))
			ans5 = request.POST.get('ans5'+str(i))


			qt = Question.objects.create(
				gp=gp,
				question=question,
				answer=answer,
				ans1=ans1,
				ans2=ans2,
				ans3=ans3,
				ans4=ans4,
				ans5=ans5
				)
			return redirect('questions:home')

	ctx={'ct':ct}
	return render(request, 'createQuiz.html',ctx)


@login_required(login_url='questions:userLogin')
def edit(request,slug):
	gp = QuestionGp.objects.get(gp_slug=slug)
	questions = gp.question_set.all()
	ct = Category.objects.all()
	user = request.user.answerer
	
	if request.method == 'POST':
		cate = request.POST.get('category')
		gp_name = request.POST.get('gp_name')
		start = int(len(questions))
		print(start)
		counter = request.POST.get('counter')
		cat = Category.objects.get(id=cate)
		gp.category = cat
		gp.gp_name = gp_name
		if counter:
			end = start+int(counter)
			for i in range(start,end):
				question = request.POST.get('question'+str(i))
				answer = request.POST.get('answer'+str(i))
				ans1 = request.POST.get('ans1'+str(i))
				ans2 = request.POST.get('ans2'+str(i))
				ans3 = request.POST.get('ans3'+str(i))
				ans4 = request.POST.get('ans4'+str(i))
				ans5 = request.POST.get('ans5'+str(i))
				print(question)
				Question.objects.create(
					gp=gp,
					question=question,
					answer=answer,
					ans1=ans1,
					ans2=ans2,
					ans3=ans3,
					ans4=ans4,
					ans5=ans5
					)
		gp.save()


		return redirect('questions:home')
			

	ctx = {'gp':gp,'questions':questions,'ct':ct}
	return render(request, 'edit.html',ctx)

@login_required(login_url='questions:userLogin')
def editQuestion(request,slug):
	question = Question.objects.get(qt_slug=slug)
	gp = question.gp.gp_slug
	if request.method == "POST":
		qt = request.POST.get('question')
		answer = request.POST.get('answer')
		ans1 = request.POST.get('ans1')
		ans2 = request.POST.get('ans2')
		ans3 = request.POST.get('ans3')
		ans4 = request.POST.get('ans4')
		ans5 = request.POST.get('ans5')

		question.question = qt
		question.answer = answer
		question.ans1 = ans1
		question.ans2 = ans2
		question.ans3 = ans3
		question.ans4 = ans4
		question.ans5 = ans5

		question.save()
		return redirect('quizdemo-bykosi.herokuapp.com/edit/'+gp)
	

	ctx = {'question':question}
	return render(request, 'editque.html',ctx) 

@login_required(login_url='questions:userLogin')
def reanswer(request):
	data = json.loads(request.body) 
	action = data['action']
	slug = data['slug']
	if action == 'reanswer':
		usergp = UserGpPoint.objects.get(slug=slug)
		usergp.delete()
	
	return JsonResponse('asdasd',safe=False) 

@login_required(login_url='questions:userLogin')
def deletequestion(request,slug):
	item = Question.objects.get(qt_slug=slug)
	sl = item.gp.gp_slug
	if request.method == 'POST':
		item.delete()
		return redirect('quizdemo-bykosi.herokuapp.com/edit/'+sl)
	ctx = {'item':item}
	return render(request,'delete.html',ctx)

@login_required(login_url='questions:userLogin')
def deletegroup(request,slug):
	item = QuestionGp.objects.get(gp_slug=slug)
	if request.method == 'POST':
		item.delete()
		return redirect('questions:home')
	ctx = {'item':item}
	return render(request,'delete.html',ctx)