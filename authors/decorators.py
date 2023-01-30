from django.shortcuts import redirect


def no_login_required(function, redirect_url='/'):
    def _wrapper(request):  
        var = request.user.is_authenticated
        match var:
            case True:
                return redirect(redirect_url)
            case False:
                return function(request) 
    return _wrapper