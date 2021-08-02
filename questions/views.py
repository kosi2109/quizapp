from django.shortcuts import render,redirect
from .models import * 
from django.http import JsonResponse
import json 

def userLogin(request):

	return render(request ,'login.html' )



def home(request):
	gp = QuestionGp.objects.all()
	ct = Category.objects.all()
			
	ctx = {'gp':gp,'ct':ct}
	return render(request, 'index.html',ctx)


def group(request,slug):
	gp = QuestionGp.objects.get(gp_slug=slug)
	questions = gp.question_set.all()
	user = request.user.answerer

	scoreurl = f'ans-{gp.gp_slug}'
	if UserGpPoint.objects.filter(slug=scoreurl):
		gpansed = UserGpPoint.objects.get(answerer=user,slug=scoreurl)
		useranss = gpansed.useranswer_set.all()
		correctans = {}
		userans = {}
		
		coQ = 1
		coA = 1
		for i in questions:
			correctans[coQ] = i.answer
			coQ += 1
		for i in useranss:
			userans[coA] = i.answer
			coA += 1
		score = gpansed.point
		ctx={'questions':questions,'scoreurl':scoreurl,'score':score,'correctans':correctans ,'userans':userans,'gp':gp,'gpansed':gpansed}
		return render(request, 'group.html',ctx)
	
	if request.method == "POST":
		usergp = UserGpPoint.objects.create(answerer=user,gp=gp)
		cont = 0
		for i in questions:
			qans = i.answer
			cont += 1
			ans = request.POST.get('ans['+str(cont)+']')
			UserAnswer.objects.create(point=usergp,question=i,answer=ans)
			if ans != None: 
				if int(qans) == int(ans):
					usergp.point += 1
					usergp.save()
			else:
				UserGpPoint.objects.get(answerer=user,gp=gp).delete()
				return redirect('questions:home')
		return redirect('http://127.0.0.1:8000/score/'+scoreurl)

	ctx={'questions':questions,'scoreurl':scoreurl,'gp':gp}
	return render(request, 'group.html',ctx)


def ctView(request,slug):
	cct = Category.objects.get(ct_slug=slug)
	gp = QuestionGp.objects.filter(category=cct)
	ct = Category.objects.all()
	ctx = {'gp':gp,'ct':ct,'cct':cct}
	return render(request, 'ctview.html',ctx)



def score(request,slug):
	gp = UserGpPoint.objects.get(slug=slug)
	ans = gp.useranswer_set.all()
	total = len(ans)

	ctx={'gp':gp,'total':total}
	return render(request, 'score.html',ctx)



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



	ctx={'ct':ct}
	return render(request, 'createQuiz.html',ctx)



def reanswer(request):
	data = json.loads(request.body) 
	action = data['action']
	slug = data['slug']
	if action == 'reanswer':
		usergp = UserGpPoint.objects.get(slug=slug)
		usergp.delete()
	
	return JsonResponse('asdasd',safe=False) 