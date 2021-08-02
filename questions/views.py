from django.shortcuts import render,redirect
from .models import * 

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

	scoreurl = f'ans-{gp.gp_slug}'
	if UserGpPoint.objects.filter(slug=scoreurl):
		gpansed = UserGpPoint.objects.get(slug=scoreurl)
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
		ctx={'questions':questions,'scoreurl':scoreurl,'score':score,'correctans':correctans ,'userans':userans}
		return render(request, 'group.html',ctx)
	user = request.user.answerer
	
	
	
	if request.method == "POST":
		usergp = UserGpPoint.objects.create(answerer=user,gp=gp)
		cont = 0
		for i in questions:
			qans = i.answer
			cont += 1
			ans = request.POST.get('ans['+str(cont)+']')
			print(cont,'ct')
			print(ans)
			UserAnswer.objects.create(point=usergp,question=i,answer=ans)
			if int(qans) == int(ans):
				usergp.point += 1
				usergp.save()
		return redirect('http://127.0.0.1:8000/score/'+scoreurl)

	ctx={'questions':questions,'scoreurl':scoreurl}
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
