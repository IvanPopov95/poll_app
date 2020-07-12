from django import forms
from .models import Question, Poll, Answer, AnswerStorage

class CreatePollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('title', 'end', 'description')

class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('poll', 'body', 'question_type')

class CreateAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('question','answer_text')

class AnswerTextForm(forms.ModelForm):
    class Meta:
        model = AnswerStorage
        fields = ('answer',)