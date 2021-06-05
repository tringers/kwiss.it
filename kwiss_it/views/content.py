from .helper import *

def add_content(request,args=None):
	if not args:
		args = {
			'errorMsg': '',
			'infoMsg': ''
		}


	return render(request, 'kwiss_it/submitusercontent.html', args)