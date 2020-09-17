from django.test import TestCase
from gradpro.forms import UserForm

class UserFormTest(TestCase):
    def test_user_form_email(self):
        form = UserForm()
        self.assertTrue(form.fields['email'].label == None or form.fields['email'].label == 'Email')

    def test_user_form_password(self):
        form = UserForm()
        self.assertTrue(form.fields['password'].label == None or form.fields['password'].label == 'Password')

    def test_user_form_first_name(self):
        form = UserForm()
        self.assertTrue(form.fields['first_name'].label == None or form.fields['first_name'].label == 'First name')

    def test_teacher_form_last_name(self):
        form = UserForm()
        self.assertTrue(form.fields['last_name'].label == None or form.fields['last_name'].label == 'Last name')