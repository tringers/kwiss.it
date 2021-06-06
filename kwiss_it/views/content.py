from .helper import *


def add_content(request, args=None):
	if not args:
		args = {
			'errorMsg': '',
			'infoMsg': ''
		}
	if request.method != 'POST':
		return render(request, 'kwiss_it/submitusercontent.html', args)

	input_questionnumberfields = request.POST.getlist("questionnumberfield")
	input_category: str = request.POST.get("category")
	c_obj = None
	input_catname = request.POST.get("catname")
	input_catdesc = request.POST.get("catdesc")
	if not check_valid_chars(input_catname):
		args["errorMsg"] = "Kategorie Namen beinhaltet nicht erlaubte Zeichen"
		return render(request, 'kwiss_it/submitusercontent.html', args)
	if not check_valid_chars(input_catdesc):
		args["errorMsg"] = "Kategoriene Beschreibung beinhaltet nicht erlaubte zeichen"
		return render(request, 'kwiss_it/submitusercontent.html', args)
	if input_category == "new":
		c_obj = Category.objects.create(Uid=request.user, Cname=input_catname, Cdescription=input_catdesc, STid=State.objects.get(STid=3))
		c_obj.save()
	else:
		if not input_category.isnumeric():
			args["errorMsg"] = "ausgewählte Kategorie ist fehlerhaft"
			return render(request, 'kwiss_it/submitusercontent.html', args)
		input_category: int = int(input_category)
		c_obj = Category.objects.get(Cid=input_category)

	for i in input_questionnumberfields:
		input_questiontext = request.POST.get("questiontext" + i)
		input_qtype = request.POST.get("qtype" + i)
		if not check_valid_chars(input_questiontext):
			args["errorMsg"] = "Fragetext beinhaltet nicht erlaubte zeichen"
			return render(request, 'kwiss_it/submitusercontent.html', args)
		if not check_valid_chars(input_qtype):
			args["errorMsg"] = "Fragen Typ ist fehlerhaft"
			return render(request, 'kwiss_it/submitusercontent.html', args)
		qt_obj = QuestionType.objects.get(QTname=input_qtype)
		q_obj = Question.objects.create(Cid=c_obj, Uid=request.user, Qtext=input_questiontext, STid=State.objects.get(STid=3), QTid=qt_obj)

		input_answeramountfield = request.POST.get("answeramountfield" + i)
		if input_answeramountfield is None:
			args["errorMsg"] = "Fehlerhafte antwortenmenge bei frage " + i
			return render(request, 'kwiss_it/submitusercontent.html', args)
		if not input_answeramountfield.isnumeric():
			args["errorMsg"] = "Fehlerhafte antwortenmenge bei frage " + i
			return render(request, 'kwiss_it/submitusercontent.html', args)
		input_answeramountfield = int(input_answeramountfield)
		answers = []
		for a in range(input_answeramountfield):
			input_answernumberfield = request.POST.get("question" + i + "answernumberfield" + str(a))
			if input_answernumberfield != str(a):
				args["errorMsg"] = "antwort feld nicht in richtiger "
				return render(request, 'kwiss_it/submitusercontent.html', args)
			if not input_answernumberfield:
				args["errorMsg"] = "Fehler in Antwortübertragung"
				return render(request, 'kwiss_it/submitusercontent.html', args)
			input_correct = ""
			if qt_obj.QTname == "number_exact" or qt_obj.QTname == "number_deviation" or qt_obj.QTname == "single":
				input_correct = request.POST.get("question" + i + "correct")
			else:
				teststring="question" + i + "correct" + str(a)
				input_correct = request.POST.get("question" + i + "correct" + str(a))
			if input_correct == str(a):
				input_correct = True
			else:
				input_correct = False
			input_answertext = request.POST.get("question" + i + "answertext" + str(a))
			if not check_valid_chars(input_answertext):
				args["errorMsg"] = f"Im Antworttext bei Frage {i} in Antwort {str(a)} sind nicht erlaubte Zeichen enthalten"
				return render(request, 'kwiss_it/submitusercontent.html', args)
			a_obj = Answer.objects.create(Acorrect=input_correct, Atext=input_answertext, Anum=input_answernumberfield, Qid=q_obj)
			answers.append(a_obj)
		if len(answers) > 0:
			q_obj.save()
			for a_obj in answers:
				a_obj.save()

	"""for key, value in request.POST.items():
		print(key)
		print(value)"""
	return render(request, 'kwiss_it/submitusercontent.html', args)
