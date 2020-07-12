from django.contrib import admin

from .models import Poll, Question, Answer

class QuestionInLine(admin.TabularInline):
    model = Question
    extra = 2

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,{'fields':
    ['title', 'description']}),
        ('Date information', {'fields':
    ['end']}),
    ]
    inlines = [QuestionInLine]
    list_display = ('title', 'end', 'is_active')

class AnswerInLine(admin.TabularInline):
    model = Answer
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInLine]
    
admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)