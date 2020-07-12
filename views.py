from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Poll, Question, Answer, AnswerStorage
from .forms import CreatePollForm, CreateQuestionForm, CreateAnswerForm, AnswerTextForm
from django.contrib.auth.decorators import user_passes_test
from django.forms import formset_factory, inlineformset_factory

class PollListView(ListView):
    model = Poll
    template_name = 'polls/index.html'
    queryset = Poll.objects.filter(is_active=True)
    paginate_by = 5

def poll_detail_view(request, poll_id):
    template = 'polls/detail_view.html'
    poll = get_object_or_404(Poll, pk=poll_id)
    questions = poll.questions.filter()
    return render (request, template, {"poll" : poll,
                                      "questions" : questions})

def question_detail_view(request, question_id):
    template = 'polls/detail_question.html'
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answer.filter()

    if request.method == 'POST':   
        if question.question_type == 1:
            new_text_answer = None
            form = AnswerTextForm(request.POST)
            if form.is_valid() and request.user:
                new_text_answer = form.save(commit=False)
                new_text_answer.user = request.user
                new_text_answer.question = question
                new_text_answer.save()
        else:
            selected_answers_pks = question.answer_set.getlist(pk=request.POST['answer'])
            selected_answers = Answer.objects.filter(pk__in=selected_answers_pks)
            if request.user:
                users_answers = AnswerStorage(answer=selected_answers, user=auth.user, question=question)
                users_answers.save()
    else :
        form = AnswerTextForm()
    return render(request, template, {'form' : form,
                       'question' : question, 
                       'new_text_answer' : new_text_answer,
                       'answers' : answers})           


def staff_check(user):
    return user.is_staff
    
@user_passes_test(staff_check)
def poll_create_view(request):
    template = 'polls/create_poll.html'
    form = CreatePollForm(request.POST or None)
    if form.is_valid():
        poll = form.save(commit=False)
        poll.author = request.user
        poll.save()
        return redirect('create_questions')
    return render(request, template, {'form' : form})


@user_passes_test(staff_check)
def questions_create_view(request, poll_id):
    template = 'polls/create_questions.html'
    poll = get_object_or_404(Poll, pk=poll_id)
    QuestionFormSet = formset_factory(CreateQuestionForm, extra=poll.questions_quantity, can_delete=True)
    if request.method == "POST":
        formset = QuestionFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
    else:
        formset = QuestionFormSet()
    return render(request, template, {'poll' : poll,
                                      'formset': formset})


@user_passes_test(staff_check)
def answers_create_view(request, question_id):
    template = 'polls/create_answers.html'
    question = get_object_or_404(Question, pk=question_id)
    AnswersFormSet = formset_factory(CreateAnswerForm, extra=4, can_delete=True )
    if request.method == "POST":
        formset = AnswersFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
    else:
        formset = AnswersFormSet()
    return render(request, template, {'question' : question,
                                      'formset': formset})


@user_passes_test(staff_check)
def update_and_delete_poll_view(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'POST':
        poll_form = CreatePollForm(request.POST, instance=poll)
        QuestionFormSet = inlineformset_factory(Poll, Question)
        question_formset = QuestionFormSet(instance=poll)
        if poll_form.is_valid() and question_formset.is_valid():
            poll_form.save()
            question_formset.save()
    else:
        poll_form = CreatePollForm(request.POST, instance=poll)
        QuestionFormSet = inlineformset_factory(Poll, Question)
        question_formset = QuestionFormSet(instance=poll)
    return render(request, 'polls/update_delete_poll.html', {
                                            'poll_form': poll_form,
                                            'question_formset': question_formset})

def profile_view(request):
    template_name = 'blog/user_page.html'
    user = request.user
    user_answers = AnswerStorage.objects.filter(user=user)
    return render(request, template_name, {'user_answers': user_answers})