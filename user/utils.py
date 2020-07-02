from django.contrib.auth.models import User
from django.db import IntegrityError
def add_new_user(name, password):
    """
    Tries to add a new user in base and return Boolean and message
        True = Success / False = Fail
    """
    try:
        new_user = User(username=name)
        new_user.set_password(password)
        new_user.save()
        return True, f"Félicitation vous venez de créer : {name} !"
    except IntegrityError:
        return False, "Cet utilisateur existe déjà !"