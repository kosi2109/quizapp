from django.db import models
import uuid
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
	ct_name = models.CharField(max_length=100,null=True)
	ct_slug = models.SlugField(unique=True,blank=True)

	def save(self,*args, **kwargs):
		uid = uuid.uuid4().hex[:5]
		self.ct_slug = uid
		while Category.objects.filter(ct_slug=self.ct_slug).exists():
			self.ct_slug = uid
		super().save(*args, **kwargs)

	def __str__(self):
		return self.ct_name

class QuestionGp(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE , null=True)
	gp_name = models.CharField(max_length=100, null=True)
	gp_slug = models.SlugField(editable = False ,unique=True,blank=True)

	def save(self,*args, **kwargs):
		if not self.gp_slug:
			ct = self.category.ct_name
			ctl = ct.replace(" ","")
			print(ctl)
			uid = uuid.uuid4().hex[:5]
			self.gp_slug = f'{ctl}_{uid}'

		super().save(*args, **kwargs) 

	def __str__(self):
		return self.gp_name

class Question(models.Model):
	gp = models.ForeignKey(QuestionGp, on_delete=models.CASCADE,null=True)
	question = models.TextField()
	answer = models.IntegerField(null=True)
	ans1 = models.CharField(max_length=100,null=True,blank=True)
	ans2 = models.CharField(max_length=100,null=True,blank=True)
	ans3 = models.CharField(max_length=100,null=True,blank=True)
	ans4 = models.CharField(max_length=100,null=True,blank=True)
	ans5 = models.CharField(max_length=100,null=True,blank=True)
	qt_slug = models.SlugField(editable = False ,unique=True,blank=True)

	def save(self,*args, **kwargs):
		if not self.qt_slug:
			gp = self.gp.gp_name
			uid = uuid.uuid4().hex[:5]
			self.qt_slug = f'{gp}-{uid}'
			while Question.objects.filter(qt_slug=self.qt_slug).exists():
				uid = uuid.uuid4().hex[:5]
				self.qt_slug = f'{gp}-{uid}'
		super().save(*args, **kwargs)



	def __str__(self):
		return self.question

class Answerer(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	name = models.CharField(max_length=200,null=True)
	email = models.CharField(max_length=200,null=True,blank=True)

	def __str__(self):
		return self.name

class UserGpPoint(models.Model):
	answerer = models.ForeignKey(Answerer,on_delete=models.CASCADE)
	gp = models.ForeignKey(QuestionGp, on_delete=models.CASCADE)
	point = models.PositiveIntegerField(default=0 ,editable=False)
	slug = models.SlugField(editable=False,blank=True)

	def save(self,*args, **kwargs):
		if not self.slug:
			self.slug = f'ans-{self.gp.gp_slug}' 
		super().save(*args, **kwargs)

	def __str__(self):
		return self.answerer.name




class UserAnswer(models.Model):
	point = models.ForeignKey(UserGpPoint,on_delete=models.CASCADE)
	question = models.OneToOneField(Question, on_delete=models.CASCADE)
	answer = models.IntegerField(null=True)
	

	def __str__(self):
		return self.question.question






