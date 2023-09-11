from django.shortcuts import render, get_object_or_404
from ..models import Question
from django.core.paginator import Paginator
from django.db.models import Q


def index(request):
    print(f"request : {request}")
    page = request.GET.get("page", "1")  # 페이지
    query = request.GET.get("kw")

    if query:
        question_list = Question.objects.filter(subject__icontains=query).order_by(
            "-create_date"
        )
    else:
        question_list = Question.objects.order_by("-create_date")

    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)  # 몇페이지 보여줄건지
    context = {"question_list": page_obj}
    print("page number : ", page_obj.number)
    return render(request, "pybo/question_list.html", context)


def detail(request, question_id, answer_id=None):
    print(f"request: {request}")
    question = get_object_or_404(Question, pk=question_id)
    if answer_id is None:
        context = {"question": question}
    else:
        context = {"question": question, "answer_id": answer_id}

    print(f"answer_pk in detail : {answer_id}")
    print(f"context :{context}")
    return render(request, "pybo/question_detail.html", context)
