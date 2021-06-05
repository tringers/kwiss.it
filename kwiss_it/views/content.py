from .helper import *

def add_content(request,args=None):
	if not args:
		args = {
			'errorMsg': '',
			'infoMsg': ''
		}
	if request.method != 'POST':
		return render(request, 'kwiss_it/submitusercontent.html', args)

	input_question_amount = request.POST.get("answeramountfield1")
	args['infoMsg']=input_question_amount


	print(input_question_amount)
	return render(request, 'kwiss_it/submitusercontent.html', args)
