from django.db import models
from .manager import UserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), blank=False, unique=True)
    first_name = models.CharField(max_length=30, blank=False, default='')
    last_name = models.CharField(max_length=30, blank=False, default='')
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


# The response model for the general metaskills test
class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# Models for the general metaskills test
class SelfManagement(models.Model):
    response = models.OneToOneField(Response, on_delete=models.CASCADE, primary_key=True,)
    # General score
    score = models.IntegerField()
    # Each dimension/subskill has its own score
    concentration_score = models.IntegerField()
    adaptability_score = models.IntegerField()
    initiative_score = models.IntegerField()

    # The questions of the model
    c_q1 = models.IntegerField()
    c_q2 = models.IntegerField()
    c_q3 = models.IntegerField()
    a_q1 = models.IntegerField()
    i_q1 = models.IntegerField()
    i_q2 = models.IntegerField()
    i_q3 = models.IntegerField()
    i_q4 = models.IntegerField()


class SocialIntelligence(models.Model):
    response = models.OneToOneField(Response, on_delete=models.CASCADE, primary_key=True, )
    score = models.IntegerField()
    communication_score = models.IntegerField()
    collaborating_score = models.IntegerField()
    feeling_score = models.IntegerField()

    com_q1 = models.IntegerField()
    com_q2 = models.IntegerField()
    com_q3 = models.IntegerField()
    com_q4 = models.IntegerField()
    col_q1 = models.IntegerField()
    col_q2 = models.IntegerField()
    col_q3 = models.IntegerField()
    col_q4 = models.IntegerField()
    f_q1 = models.IntegerField()


class Innovation(models.Model):
    response = models.OneToOneField(Response, on_delete=models.CASCADE, primary_key=True, )
    score = models.IntegerField()
    sense_making_score = models.IntegerField()
    curiosity_score = models.IntegerField()
    creativity_score = models.IntegerField()
    critical_thinking_score = models.IntegerField()

    s_q1 = models.IntegerField()
    s_q2 = models.IntegerField()
    s_q3 = models.IntegerField()
    s_q4 = models.IntegerField()
    s_q5 = models.IntegerField()
    cu_q1 = models.IntegerField()
    cu_q2 = models.IntegerField()
    cu_q3 = models.IntegerField()
    cu_q4 = models.IntegerField()
    crea_q1 = models.IntegerField()
    crit_q1 = models.IntegerField()


# The response model for the communication test
class ComResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# The communication test model
class Communication(models.Model):
    response = models.OneToOneField(ComResponse, on_delete=models.CASCADE, primary_key=True, )
    score = models.IntegerField(null=True, blank=True)
    social_composure_score = models.IntegerField(null=True, blank=True)
    social_confirmation_score = models.IntegerField(null=True, blank=True)
    social_experience_score = models.IntegerField(null=True, blank=True)
    appropriate_disclosure_score = models.IntegerField(null=True, blank=True)
    articulation_score = models.IntegerField(null=True, blank=True)
    wit_score = models.IntegerField(null=True, blank=True)

    q1 = models.IntegerField(null=True, blank=True)
    q2 = models.IntegerField(null=True, blank=True)
    q3 = models.IntegerField(null=True, blank=True)
    q4 = models.IntegerField(null=True, blank=True)
    q5 = models.IntegerField(null=True, blank=True)
    q6 = models.IntegerField(null=True, blank=True)
    q7 = models.IntegerField(null=True, blank=True)
    q8 = models.IntegerField(null=True, blank=True)
    q9 = models.IntegerField(null=True, blank=True)
    q10 = models.IntegerField(null=True, blank=True)
    q11 = models.IntegerField(null=True, blank=True)
    q12 = models.IntegerField(null=True, blank=True)
    q13 = models.IntegerField(null=True, blank=True)
    q14 = models.IntegerField(null=True, blank=True)
    q15 = models.IntegerField(null=True, blank=True)
    q16 = models.IntegerField(null=True, blank=True)
    q17 = models.IntegerField(null=True, blank=True)
    q18 = models.IntegerField(null=True, blank=True)
    q19 = models.IntegerField(null=True, blank=True)
    q20 = models.IntegerField(null=True, blank=True)
    q21 = models.IntegerField(null=True, blank=True)
    q22 = models.IntegerField(null=True, blank=True)
    q23 = models.IntegerField(null=True, blank=True)
    q24 = models.IntegerField(null=True, blank=True)
    q25 = models.IntegerField(null=True, blank=True)
    q26 = models.IntegerField(null=True, blank=True)
    q27 = models.IntegerField(null=True, blank=True)
    q28 = models.IntegerField(null=True, blank=True)
    q29 = models.IntegerField(null=True, blank=True)
    q30 = models.IntegerField(null=True, blank=True)


# The response model for the adaptability test
class AdaResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# The adaptability test model
class Adaptability(models.Model):
    response = models.OneToOneField(AdaResponse, on_delete=models.CASCADE, primary_key=True, )
    score = models.IntegerField(null=True, blank=True)
    crisis_score = models.IntegerField(null=True, blank=True)
    work_stress_score = models.IntegerField(null=True, blank=True)
    creativity_score = models.IntegerField(null=True, blank=True)
    uncertainty_score = models.IntegerField(null=True, blank=True)
    learning_score = models.IntegerField(null=True, blank=True)
    interpersonal_score = models.IntegerField(null=True, blank=True)
    cultural_score = models.IntegerField(null=True, blank=True)
    physical_score = models.IntegerField(null=True, blank=True)

    q1 = models.IntegerField(null=True, blank=True)
    q2 = models.IntegerField(null=True, blank=True)
    q3 = models.IntegerField(null=True, blank=True)
    q4 = models.IntegerField(null=True, blank=True)
    q5 = models.IntegerField(null=True, blank=True)
    q6 = models.IntegerField(null=True, blank=True)
    q7 = models.IntegerField(null=True, blank=True)
    q8 = models.IntegerField(null=True, blank=True)
    q9 = models.IntegerField(null=True, blank=True)
    q10 = models.IntegerField(null=True, blank=True)
    q11 = models.IntegerField(null=True, blank=True)
    q12 = models.IntegerField(null=True, blank=True)
    q13 = models.IntegerField(null=True, blank=True)
    q14 = models.IntegerField(null=True, blank=True)
    q15 = models.IntegerField(null=True, blank=True)
    q16 = models.IntegerField(null=True, blank=True)
    q17 = models.IntegerField(null=True, blank=True)
    q18 = models.IntegerField(null=True, blank=True)
    q19 = models.IntegerField(null=True, blank=True)
    q20 = models.IntegerField(null=True, blank=True)
    q21 = models.IntegerField(null=True, blank=True)
    q22 = models.IntegerField(null=True, blank=True)
    q23 = models.IntegerField(null=True, blank=True)
    q24 = models.IntegerField(null=True, blank=True)
    q25 = models.IntegerField(null=True, blank=True)
    q26 = models.IntegerField(null=True, blank=True)
    q27 = models.IntegerField(null=True, blank=True)
    q28 = models.IntegerField(null=True, blank=True)
    q29 = models.IntegerField(null=True, blank=True)
    q30 = models.IntegerField(null=True, blank=True)
    q31 = models.IntegerField(null=True, blank=True)
    q32 = models.IntegerField(null=True, blank=True)
    q33 = models.IntegerField(null=True, blank=True)
    q34 = models.IntegerField(null=True, blank=True)
    q35 = models.IntegerField(null=True, blank=True)
    q36 = models.IntegerField(null=True, blank=True)
    q37 = models.IntegerField(null=True, blank=True)
    q38 = models.IntegerField(null=True, blank=True)
    q39 = models.IntegerField(null=True, blank=True)
    q40 = models.IntegerField(null=True, blank=True)
    q41 = models.IntegerField(null=True, blank=True)
    q42 = models.IntegerField(null=True, blank=True)
    q43 = models.IntegerField(null=True, blank=True)
    q44 = models.IntegerField(null=True, blank=True)
    q45 = models.IntegerField(null=True, blank=True)
    q46 = models.IntegerField(null=True, blank=True)
    q47 = models.IntegerField(null=True, blank=True)
    q48 = models.IntegerField(null=True, blank=True)
    q49 = models.IntegerField(null=True, blank=True)
    q50 = models.IntegerField(null=True, blank=True)
    q51 = models.IntegerField(null=True, blank=True)
    q52 = models.IntegerField(null=True, blank=True)
    q53 = models.IntegerField(null=True, blank=True)
    q54 = models.IntegerField(null=True, blank=True)
    q55 = models.IntegerField(null=True, blank=True)
