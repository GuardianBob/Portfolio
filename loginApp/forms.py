from .models import User
from django import forms
import datetime
import bcrypt

class Register_Form(forms.Form):
    first_name = forms.CharField(max_length=200, widget=forms.TextInput)
    last_name = forms.CharField(max_length=200, widget=forms.TextInput)  
    email = forms.EmailField(max_length=200, widget=forms.EmailInput)
    reg_password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput)
    check_pass_r = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(Register_Form, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class' : 'form-control',
            })
        self.fields['reg_password'].widget.attrs.update({
            'id': 'reg_password',
        })
        self.fields['check_pass_r'].widget.attrs.update({
            'class' : 'form-control',
            'id': 'check_pass_r',
            'onChange': 'checkPass();'
        })
        self.fields['reg_password'].label = 'Password'
        self.fields['check_pass_r'].label = 'Password Confirmation'

    def clean(self):
        super(Register_Form, self).clean()
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        # password = self.cleaned_data.get('reg_password')
        # check_pass_r = self.cleaned_data.get('check_pass_r')
        
        def check_string(string, length, varName):
            if len(string) < length: 
                self.errors[f"{varName}"] = self.error_class([
                    f'Input must be at least 2 characters.'])

        check_string(first_name, 2, 'first_name')
        check_string(last_name, 3, 'last_name')

        if len(User.objects.filter(email=email)) > 0: 
                self.errors[f"email"] = self.error_class([
                    f'This email already exists in the system'])
        return self.cleaned_data

class Login_Form(forms.Form): 
    login_email = forms.EmailField(max_length=200, widget=forms.EmailInput)
    login_password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(Login_Form, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class' : 'form-control',
            })
            self.fields['login_password'].widget.attrs.update({
                'class' : 'form-control',
                'id' : 'login_password',
                'onChange': 'passEnbl();'
            })
            self.fields['login_password'].label = 'Password'

    def clean(self):
        super(Login_Form, self).clean()
        email = self.cleaned_data.get('login_email')
        password = self.cleaned_data.get('login_password')

        if not len(User.objects.filter(email=email)) > 0:
            self.errors[f'login_email'] = self.error_class([
                    f'Email or password is invalid'])
        else:
            stored_data = User.objects.get(email=email)
            if not bcrypt.checkpw(password.encode(), stored_data.password.encode()):
                self.errors[f'login_email'] = self.error_class([
                    f'Email or password is invalid'])
        return self.cleaned_data