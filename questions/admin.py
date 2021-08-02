from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Category)
admin.site.register(QuestionGp)
admin.site.register(Question)
admin.site.register(Answerer)

admin.site.register(UserAnswer)

class GpaAdmin(admin.ModelAdmin):
	list_display = ('answerer','gp','point')

admin.site.register(UserGpPoint , GpaAdmin)
