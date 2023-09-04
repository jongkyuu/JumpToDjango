from django.shortcuts import render, get_object_or_404
from ..models import Question
from django.core.paginator import Paginator


def index(request):
    page = request.GET.get("page", "1")  # 페이지
    question_list = Question.objects.order_by("-create_date")
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)  # 몇페이지 보여줄건지
    context = {"question_list": page_obj}
    print("page number : ", page_obj.number)
    return render(request, "pybo/question_list.html", context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {"question": question}
    return render(request, "pybo/question_detail.html", context)
