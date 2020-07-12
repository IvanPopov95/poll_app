from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Poll(models.Model):
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    title = models.CharField(max_length=100)
    start = models.DateTimeField(default=timezone.now, editable=False)
    end = models.DateTimeField(null=True)
    description = models.TextField()
    questions_quantity = models.IntegerField()

    def is_active(self):
        now = timezone.now()
        return self.end > now

    def __str__(self):
        return self.title

class Question(models.Model):
    TYPE_CHOICES = (
        (1, 'text'),
        (2, 'one answer'),
        (3, 'many answers'),
    )
    body = models.TextField()
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    question_type = models.IntegerField(choices=TYPE_CHOICES, default=1)

    def __str__(self):
        return '{0} - question from poll {1}'.format(self.body, self.poll)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(max_length=200)

class AnswerStorage(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField()

    def __str__(self):
        return 'Answer for question {0} '.format(self.question)