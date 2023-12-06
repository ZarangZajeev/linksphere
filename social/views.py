from django.shortcuts import render, redirect
from django.views.generic import View, FormView, CreateView, TemplateView, UpdateView
from social.form import RegistrationForm, LoginForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from social.models import UserProfile

# Create your views here.
class SignUpView(CreateView):
    template_name="register.html"
    form_class=RegistrationForm

    def get_success_url(self):
        return reverse("signin")

    # def post(self,request,*args,**kwargs):
    #     form=RegistrationForm(request.POST)
    #     if form.is_valid:
    #         form.save()
    #         return redirect("signup")
    #     else:
    #         return render(request,"register.html",{"from":form})

class SigninView(FormView):
    template_name="login.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_obj=authenticate(request,username=uname,password=pwd)
            if user_obj:
                login(request,user_obj)
                print("Login successfully")
                return redirect("index")
        print("Failed to login")
        return render(request,"login.html",{"form":form})
    
class IndexView(TemplateView):
    template_name="index.html"


class SignoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    
class ProfileUpdateView(UpdateView):
    template_name="profile_edit.html"
    form_class=UserProfileForm
    model=UserProfile

    def get_success_url(self):
        return reverse("index")