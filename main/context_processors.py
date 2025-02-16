

def current_user_context(request):
    return {
        'current_user': request.user
    }

