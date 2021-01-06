from django.contrib.auth.models import User

def manage_auth_error(username, context): 
    does_this_user_exists = len(User.objects.filter(username=username)) > 0
    if does_this_user_exists: #issue with user
        context['error'] = "Cet utilisateur n'existe pas"
    else:
        context['error'] = "le mot de passe n'est pas bon"
        return context