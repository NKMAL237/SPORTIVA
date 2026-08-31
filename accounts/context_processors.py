from accounts.decorators import DEFAULT_GUEST_TABS

def tab_access(request):
    """
    Context processor providing allowed_tabs list to all templates.
    """
    if request.user.is_authenticated:
        allowed = request.user.get_allowed_tabs()
    else:
        allowed = DEFAULT_GUEST_TABS

    return {
        'allowed_tabs': allowed,
    }
