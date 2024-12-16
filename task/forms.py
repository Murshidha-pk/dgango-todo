from django import forms

from task.models import User,Todo

from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):

    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mb-2"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mb-2"}))

    class Meta:

        model=User

        fields=["username","email","password1","password2","phone"]

        widgets={

            "username":forms.TextInput(attrs={"class":"form-control mb-2"}),
            "email":forms.EmailInput(attrs={"class":"form-control mb-2"}),
            "phone":forms.NumberInput(attrs={"class":"form-control mb-2"})

        }


class SignInForm(forms.Form):

   username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-2"}))

   password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mb-2"}))

#todo form

class TodoForm(forms.ModelForm):

    class Meta:

        model=Todo

        fields=["title"]