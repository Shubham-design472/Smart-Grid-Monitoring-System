# monitoring/decorators.py
from django.http import HttpResponseForbidden
from functools import wraps

# monitoring/decorators.py

def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")
            
            # FIX: Access role via the 'profile' relationship
            # We use getattr/hasattr to be safe in case a user has no profile
            if hasattr(request.user, 'profile') and request.user.profile.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            return HttpResponseForbidden("You are not authorized to access this page.")
        return _wrapped_view
    return decorator

