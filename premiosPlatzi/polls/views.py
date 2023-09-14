from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic

from .models import Question,Choices

# Create your views here.

#index es una function based view
# def index(request):
#     latest_question_list = Question.objects.all()
#     return render(request,"polls/index.html", {
#         "latest_question_list":latest_question_list
#     })


# def detail(request, question_id):
#     question= get_object_or_404(Question,pk=question_id)
#     return render(request,"polls/detail.html",{
#         "question":question
#     })


# def results(request, question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request, "polls/results.html",{"question":question})

#Cambio mis fuction based views por class based views(Generic views)
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """retorna las ultimas 5 preguntas"""
        return Question.objects.order_by("-pubdate")[:5]

class DetalView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choices_set.get(pk=request.POST["choice"])
    except(KeyError,Choices.DoesNotExist):
        return render(request,"polls/detail.html",
                      {
                          "question":question,
                          "error_mesage":"No elegiste una respuesta"
                      })
    else:
        selected_choice.votes = F("votes") + 1    #F() es para evitar race conditions
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results",args=(question.id,))) 

