from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _

DEFAULT_GUEST_TABS = ['home', 'events', 'organizations', 'media_feed', 'marketplace', 'sponsorships']

def tab_required(tab_name):
    """
    Decorator for views that checks whether the current user (or guest) has access to tab_name.
    Redirects to home page with an error message if access is denied.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                if tab_name in DEFAULT_GUEST_TABS:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.warning(request, _("Please log in to access this tab."))
                    return redirect('login')

            if request.user.has_tab_access(tab_name):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(
                    request,
                    _("Access Denied: Your account role does not have permission to access the '%(tab)s' tab.") % {'tab': tab_name.replace('_', ' ').title()}
                )
                return redirect('home')
        return _wrapped_view
    return decorator
