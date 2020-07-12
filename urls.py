from django.urls import path

from . import views

urlpatterns = [
    path('', views.PollListView.as_view, name='index'),
    path('new_poll', views.poll_create_view, name='create_poll'),
    path('<int:poll_id>/questions', views.questions_create_view, name='create_questions'),
    path('<int:poll_id>/questions/answers', views.answers_create_view, name='create_answers'),
    path('<int:poll_id>/', views.poll_detail_view, name='poll_detail'),
    path('<int:poll_id>/<int:question_id>', views.question_detail_view, name='question_detail'),
    path('<int:poll_id>/update_and_delete', views.update_and_delete_poll_view, name='poll_update'),
    path('profile_page/', views.profile_view, name='profile'),
]