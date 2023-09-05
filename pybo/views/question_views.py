from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..models import Question
from ..forms import QuestionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import time


@login_required(login_url="common:login")
def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect("pybo:index")
    else:
        form = QuestionForm()
    context = {"form": form}
    return render(request, "pybo/question_form.html", context)


@login_required(login_url="common:login")
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "수정권한이 없습니다")
        return redirect("pybo:detail", question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        print(f"form : {form}")
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect("pybo:detail", question_id=question_id)
    else:
        form = QuestionForm(instance=question)
        print(f"form : {form}")
    context = {"form": form}
    return render(request, "pybo/question_form.html", context)


@login_required(login_url="common:login")
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "삭제권한이 없습니다")
        return redirect("pybo:detail", question_id=question.id)
    question.delete()
    print(request, "삭제하였습니다")
    return redirect("pybo:index")


@login_required(login_url="common:login")
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    print(f"이미 존재하는 user인가요 : {question.voter.filter(pk=request.user.pk).exists()}")

    if question.voter.filter(pk=request.user.pk).exists():
        print("voter에 있는 user 삭제")
        question.voter.remove(request.user)
    else:
        print("voter에 user 추가")
        question.voter.add(request.user)

    for user in question.voter.all():
        print(f"user : {user}")

    time.sleep(1)
    return redirect("pybo:detail", question_id=question.id)
