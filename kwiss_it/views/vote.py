from .helper import *


def voteCat(request, cat_id, vote):
	if request.method != 'POST':
		return redirect("index")
	response_data = {}
	if not cat_id.isnumeric() or not vote.isnumeric():
		response_data['result'] = 400
		response_data['message'] = "wrong data format used"
		return JsonResponse(response_data)
	c_objs = Category.objects.filter(Cid=cat_id)

	if len(c_objs) != 1:
		response_data['result'] = 404
		response_data['message'] = "category not found"
		return JsonResponse(response_data)
	CV_objs = CategoryVotes.objects.filter(Q(Uid=request.user) & Q(Cid=c_objs))
	if len(CV_objs) == 1:
		CV_objs.vote = vote - 10
		response_data['result'] = 200
		response_data['message'] = "successfully voted"
	elif len(CV_objs) < 1:
		QuestionVotes.objects.create(Cid=c_objs, Uid=request.user, vote=vote - 10)
		response_data['result'] = 200
		response_data['message'] = "successfully voted"
	else:
		response_data['result'] = 409
		response_data['message'] = "multiple votes found for the user for this category"
	return JsonResponse(response_data)

def voteQuestion(request, q_id, vote):
	if request.method != 'POST':
		return redirect("index")
	response_data = {}
	if not q_id.isnumeric() or not vote.isnumeric():
		response_data['result'] = 400
		response_data['message'] = "wrong data format used"
		return JsonResponse(response_data)
	q_objs = Question.objects.filter(Qid=q_id)

	if len(q_objs) != 1:
		response_data['result'] = 404
		response_data['message'] = "category not found"
		return JsonResponse(response_data)
	QV_objs = QuestionVotes.objects.filter(Q(Uid=request.user) & Q(Qid=q_objs))
	if len(QV_objs) == 1:
		QV_objs.vote = vote - 10
		response_data['result'] = 200
		response_data['message'] = "successfully voted"
	elif len(QV_objs) < 1:
		QuestionVotes.objects.create(Qid=q_objs, Uid=request.user, vote=vote - 10)
		response_data['result'] = 200
		response_data['message'] = "successfully voted"
	else:
		response_data['result'] = 409
		response_data['message'] = "multiple votes found for the user for this question"
	return JsonResponse(response_data)
