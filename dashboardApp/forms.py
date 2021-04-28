from .models import Message, Comment
from loginApp.models import User
from django import forms
import datetime
from django.forms.widgets import TextInput
import bcrypt

LEVEL_SELECT = (
    ('False', 'Normal'),
    ('True', 'Admin')
)

class MessageForm(forms.Form):
    pass

class CommentForm(forms.Form):
    pass

class UpdateUserForm(forms.Form):
    # user_id = forms.CharField(max_length=200, widget=forms.TextInput)
    first_name = forms.CharField(max_length=200, widget=forms.TextInput)
    last_name = forms.CharField(max_length=200, widget=forms.TextInput)  
    email = forms.EmailField(max_length=200, widget=forms.EmailInput)
    user_level = forms.ChoiceField(widget=forms.Select, choices=LEVEL_SELECT, required=False)
    # reg_password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput, required=False)
    # check_pass_r = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)    

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class' : 'form-control',
            })
            # self.fields['description'].widget.attrs.update({
            #     'class' : 'form-control',
            #     'id': 'des',
            # })
        
    def clean(self):
        super(UpdateUserForm, self).clean()
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        user_level = self.cleaned_data.get('user_level')
                
        # def check_string(string, length, varName):
        #     if len(string) < length: 
        #         self.errors[f"{varName}"] = self.error_class([
        #             f'Input must be at least 2 characters.'])
        #         print('error failed')

        # check_string(first_name, 2, 'first_name')
        # check_string(last_name, 3, 'last_name')
                
        return self.cleaned_data

class UpdatePasswordForm(forms.Form):
    user_id = forms.CharField(max_length=200, widget=forms.TextInput)
    password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput, required=False)
    check_password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class' : 'form-control',
            })
        self.fields['password'].widget.attrs.update({
            'id': 'password',
        })
        self.fields['check_password'].widget.attrs.update({
            'class' : 'form-control',
            'id': 'check_password',
            'onChange': 'checkPass();'
        })
        self.fields['user_id'].widget.attrs.update({
            'class' : 'form-control',
            'id': 'user_id',
        })
        self.fields['password'].label = 'Password'
        self.fields['check_password'].label = 'Password Confirmation'

    def clean(self):
        super(UpdatePasswordForm, self).clean()
        password = self.cleaned_data.get('password')
        user_id = self.cleaned_data.get('user_id')
                
        user = User.objects.get(id=user_id)       

        
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            self.errors['password'] = self.error_class([
                f'Password cannot be the same as previous password.'])

        return self.cleaned_data

