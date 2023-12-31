from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from social.models import UserProfile,Posts,Comments,Stories


class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]

        widgets={
                "username":forms.TextInput(attrs={
                    "class":"form-control",
                    "placeholder":"Enter username"
                    }),
                "email":forms.EmailInput(attrs={
                    "class":"form-control",
                    "Placeholder":"Email"
                }),
        }
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder':"Enter a password",
            })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'Placeholder':'Confirm Password',
            })
        
class LoginForm(forms.Form):
    username=forms.CharField(widget=(forms.TextInput)(attrs={"class":"form-control","placeholder":"Enter username"}))
    password=forms.CharField(widget=(forms.PasswordInput)(attrs={"class":"form-control","placeholder":"Enter Password"}))
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=("user","following","block")
        widgets={
            "dob":forms.DateInput(attrs={"class":"form-control","type":"date"})
            }

class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=["title","post_image"]
        # widgets={
        #     "title":forms.TextInput(attrs={
        #         "class":"form-control"}),

        # }

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=["text"]

class StoryForm(forms.ModelForm):
    class Meta:
        model=Stories
        fields=["title","post_image"]