from .helper import *


def voteCat(request, cat_id, vote):
	if request.method != 'POST':
		return HttpResponse(400)
	if is_lazy_user(request.user):
		return HttpResponse(400)
	try:
		c_objs = Category.objects.get(Cid=cat_id)
	except Exception as e:
		return HttpResponse(400)

	CV_objs = CategoryVotes.objects.filter(Q(Uid=request.user) & Q(Cid=c_objs))
	CV_len = len(CV_objs)
	if CV_len < 1:
		obj = QuestionVotes.objects.create(Cid=c_objs, Uid=request.user, vote=vote - 10)
		obj.save()
	elif CV_len == 1:
		CV_objs.vote = vote - 10
		CV_objs.save()
	return  HttpResponse(200)

def voteQuestion(request, q_id, vote):
	if request.method != 'POST':
		return HttpResponse(404)
	if is_lazy_user(request.user):
		return HttpResponse(400)
	try:
		q_objs = Question.objects.get(Qid=q_id)
	except Exception as e:
		return HttpResponse(400)
	QV_objs = QuestionVotes.objects.filter(Q(Uid=request.user) & Q(Qid=q_objs))
	QV_len = len(QV_objs)
	if QV_len < 1:
		obj = QuestionVotes.objects.create(Qid=q_objs, Uid=request.user, vote=vote - 10)
		obj.save()

	elif QV_len == 1:
		QV_objs.vote = vote - 10
		QV_objs.save()

	return HttpResponse(200)


def stateCategory(request, c_id, state):
	if request.method != 'POST' or not request.user.is_staff:
		return redirect("moderator")
	cat_obj = Category.objects.get(c_id=c_id)
	stat_obj = State.objects.get(Sdescription=state)
	cat_obj.STid = stat_obj
	return


def stateQuestion(request, q_id, state):
	if request.method != 'POST' or not request.user.is_staff:
		return
	question_obj = Question.objects.get(q_id=q_id)
	stat_obj = State.objects.get(Sdescription=state)
	question_obj.STid = stat_obj
	return
