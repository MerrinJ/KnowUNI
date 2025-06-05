from django.http import HttpResponseRedirect

def student_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' in request.session:
            return view_func(request, *args, **kwargs)
        return HttpResponseRedirect('/login_page/?next=' + request.path)
    return wrapper
