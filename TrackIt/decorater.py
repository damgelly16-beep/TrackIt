from functools import wraps
from django.shortcuts import redirect

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_logged'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def rol_requerido(*rol):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.session.get('usuario_logged'):
                return redirect('login')
            
            user_rol = request.session.get('rol')
            if request.session.get('usuario_logged') != 'admin' and user_rol not in rol:
                return redirect('dashboard')
                
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator