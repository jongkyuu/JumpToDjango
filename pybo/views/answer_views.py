from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..models import Question, Answer
from ..forms import AnswerForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse


@login_required(login_url="common:login")
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print(f"question : {question}")
    print(f"request.user : {request.user}")
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect("pybo:detail", question_id=question.id)
    else:
        form = AnswerForm()
    context = {"question": question, "form": form}
    return render(request, "pybo/question_detail.html", context)


@login_required(login_url="common:login")
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "수정권한이 없습니다")
        return redirect("pybo:detail", question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        print(f"form : {form}")
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect("pybo:detail", question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
        print(f"form : {form}")
    context = {"form": form}
    return render(request, "pybo/answer_form.html", context)


@login_required(login_url="common:login")
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "삭제권한이 없습니다")
    else:
        answer.delete()
        print(request, "삭제하였습니다")
    return redirect("pybo:detail", question_id=answer.question.id)


@login_required(login_url="common:login")
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user == answer.author:
        messages.error(request, "본인이 작성한 글은 추천할수 없습니다")
    elif answer.voter.filter(pk=request.user.pk).exists():
        answer.voter.remove(request.user)
    else:
        answer.voter.add(request.user)
    # return redirect("pybo:detail", question_id=answer.question.id)

    # answer.voter.count 값을 가져와서 JSON 응답으로 반환
    new_count = answer.voter.count()
    response_data = {"new_count": new_count}
    print(f"response_data : {response_data}")
    return JsonResponse(response_data)
