from django.contrib.auth.models import check_password
from models import tangol_user
from django.conf import settings
from django.contrib.auth import get_user_model

class tangy_auth(object):
    """
    Authenticate using new user model defined by unique email.

    """
    def __init__(self):
        self.UserModel = get_user_model()

    def authenticate(self, email=None, password=None):
        try:
            user = self.UserModel.objects.get(email=email)
        except:
            return None

        if user:
            pwd_valid = check_password(password, user.password)
            if pwd_valid is True:
                return user
        return None

    def get_user(self, user_id):
        try:
            return self.UserModel.objects.get(pk=user_id)
        except:
            return None
