from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, FormView, CreateView, TemplateView, UpdateView, DetailView,ListView
from social.form import RegistrationForm, LoginForm, UserProfileForm,PostForm,CommentForm,StoryForm
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from social.models import UserProfile,Posts,Comments
from django.contrib import messages
from django.utils.decorators import method_decorator

# Create your views here.
# def signin_required(fn):
#     def wrapper(request,*args,**kwargs):
#         if not request.user.is_autheticated:
#             messages.error(request,"Please login")
#             return redirect("signin")
#         else:
#             return fn(request,*args,**kwargs)
#     return wrapper




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
    
# @method_decorator(signin_required,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    model=Posts
    context_object_name="data"

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("index")
    
    def get_queryset(self):
        blocked_profiles=self.request.user.profile.block.all()
        blockedprofile_id=[pr.user.id for pr in blocked_profiles]
        print(blockedprofile_id)
        qs=Posts.objects.all().exclude(user__id__in=blockedprofile_id).order_by("-created_date")
        return qs
    

# @method_decorator(signin_required,name="dispatch")
class SignoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    
# @method_decorator(signin_required,name="dispatch")
class ProfileUpdateView(UpdateView):
    template_name="profile_edit.html"
    form_class=UserProfileForm
    model=UserProfile

    def get_success_url(self):
        return reverse("index")
    
# @method_decorator(signin_required,name="dispatch")
class ProfileDetailView(DetailView):
    template_name="profile.html"
    model=UserProfile
    context_object_name="data"

    # def post(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     profile_object=UserProfile.objects.get(id=id)
    #     action=request.POST.get("action")
    #     if action=="follow":
    #         request.user.profile.following.add(profile_object)
    #     else:
    #         request.user.profile.following.remove(profile_object)
    #     return redirect("profile")

class ProfileListView(View):
    def get(self, request, *args,**kwargs):
        qs=UserProfile.objects.all().exclude(user=request.user)
        return render(request,"profile_list.html",{"data":qs})
    
class FollowView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        profile_object=UserProfile.objects.get(id=id)
        action=request.POST.get("action")
        if action=="follow":
            request.user.profile.following.add(profile_object)
        elif action=="unfollow":
            request.user.profile.following.remove(profile_object)
        return redirect("profile-list")
    
class PostLikeView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post_object=Posts.objects.get(id=id)
        action=request.POST.get("action")
        if action=="like":
            post_object.liked_by.add(request.user)
        elif action=="dislike":
            post_object.liked_by.remove(request.user)
        return redirect("index")
    
class CommentView(CreateView,ListView):
    template_name="index.html"
    form_class=CommentForm
    model=Comments
    context_object_name="data"

    def get_success_url(self):
        return reverse("index")
    
    def form_valid(self, form):
        id=self.kwargs.get("pk")
        post_object=Posts.objects.get(id=id)
        form.instance.user=self.request.user
        form.instance.post=post_object
        return super().form_valid(form)
    
class ProfileBlockView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        profile_object=UserProfile.objects.get(id=id)
        action=request.POST.get("action")
        if action=="block":
            request.user.profile.block.add(profile_object)
        elif action=="unblock":
            request.user.profile.block.remove(profile_object)
        return redirect("index")

class StoryCreateView(View):
    def post(self,request,*args,**kwargs):
        form=StoryForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect("index")
        return redirect("index")