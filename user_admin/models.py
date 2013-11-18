from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms import IntegerField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm

class TangolUserManager(BaseUserManager):
    def create_user(self, email, phone, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=TangolUserManager.normalize_email(email),
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password, first_name, last_name):
        user = self.create_user(email,
            password=password,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class tangol_user(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True, db_index=True)
    first_name = models.CharField(max_length=45, blank=False, verbose_name="firstname")
    last_name = models.CharField(max_length=45, blank=False, verbose_name="lastname")
    phone = models.BigIntegerField(db_index=True, blank=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = TangolUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'first_name', 'last_name']

#    def __init__(self):
#        self.ProfileModel = settings.AUTH_PROFILE_MODULE

    def get_full_name(self):
        # For this case we return email. Could also be User.first_name User.last_name if you have these fields
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        # For this case we return email. Could also be User.first_name if you have this field
        return self.email
    def get_email(self):
        #return user email
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Handle whether the user has a specific permission?"
        return True

    def has_module_perms(self, app_label):
        # Handle whether the user has permissions to view the app `app_label`?"
        return True

#    def get_profile(self):
#        ProfileModel = settings.AUTH_PROFILE_MODULE
#        return ProfileModel.objects.get(user_id=self.user_id)

    @property
    def is_staff(self):
        # Handle whether the user is a member of staff?"
        return self.is_admin

class NewUserForm(UserCreationForm):

    def __init__(self, *args, **kargs):
        super(NewUserForm, self).__init__(*args, **kargs)
        del self.fields['username']

    phone = IntegerField(localize=True)

    class Meta:
        model = tangol_user
        fields = ('email', 'first_name', 'last_name', 'phone')
#        exclude = ['username']


class Profile(models.Model):
    def user_pic(self, filename):
        return 'users/%s' % (user.username)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    pic = models.ImageField("Profile Picture", upload_to="users")
    city = models.CharField(max_length=250, null=True)


class Profile_Form(ModelForm):
    class Meta:
        model = Profile
        fields = ('pic', 'city')

class Settings(models.Model):
    TEXT = 1
    EMAIL = 2
    BOTH = 3
    NUDGE_BY_CHOICES = (
        (TEXT, 'Text Message'),
        (EMAIL, 'Email'),
        (BOTH, 'Email and Text Message'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    nudge_type = models.IntegerField(verbose_name='Recieve Nudges by',
                                                    choices=NUDGE_BY_CHOICES,
                                                    default=TEXT)
class Settings_Form(ModelForm):
    class Meta:
        model = Settings
        exclude = ['user']

