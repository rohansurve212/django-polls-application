from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import QuerySet
from .models import Question
from django.http import Http404


def index(request: HttpRequest) -> HttpResponse:
    # SELECT * FROM polls_questions ORDER BY pub_date DESC LIMIT 5
    latest_question_list: QuerySet[Question] = Question.objects.order_by(
        '-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request: HttpRequest, question_id: int) -> HttpResponse:
    question = question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request: HttpRequest, question_id: int) -> HttpResponse:
    response = HttpResponse(
        f"You're looking at the results of question {question_id}.")
    return response


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    return HttpResponse(f"You're voting on question {question_id}.")
