from django.shortcuts import render, reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, response
from django.contrib.auth.models import Group, User
from App_auth.forms import *
from App_auth.models import *
from App_main.forms import *
from App_main.models import *
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
def is_freelancer(user):
    return user.groups.filter(name='Freelancer').exists()


def is_buyer(user):
    return user.groups.filter(name='Buyer').exists()


def is_profile_filled(user):
    if is_freelancer(user):
        profile = FreelancerProfileModel.objects.filter(user=user).exists()
        return profile
    elif is_buyer(user):
        profile = BuyerProfileModel.objects.filter(user=user).exists()
        return profile


def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if is_freelancer(user):
                return HttpResponseRedirect(reverse('App_main:freelancer-home'))
            elif is_buyer(user):
                return HttpResponseRedirect(reverse('App_main:buyer-home'))
    content = {
        'form': form,
    }
    return render(request, 'App_auth/login.html', context=content)


def registration_view(request):
    form = RegistrationForm()
    if request.method == 'POST':
        grp = request.POST.get('grp')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User(username=email)
        user.set_password(password)
        user.save()
        thisGroup = Group.objects.get_or_create(name=grp)
        thisGroup[0].user_set.add(user)
        return HttpResponseRedirect(reverse('App_auth:login'))
    content = {
        'form': form,
    }
    return render(request, 'App_auth/registration.html', context=content)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_auth:login'))


def profile_setup_view(request):
    if is_freelancer(request.user):
        form = FreelancerProfileModelForm()
        if request.method == 'POST':
            form = FreelancerProfileModelForm(request.POST, request.FILES)
            if form.is_valid():
                thisForm = form.save(commit=False)
                thisForm.user = request.user
                thisForm.activity_status = True
                thisForm.save()
                return HttpResponseRedirect(reverse('App_main:freelancer-home'))
    elif is_buyer(request.user):
        form = BuyerProfileModelForm()
        if request.method == 'POST':
            form = BuyerProfileModelForm(request.POST, request.FILES)
            if form.is_valid():
                thisForm = form.save(commit=False)
                thisForm.user = request.user
                thisForm.save()
                return HttpResponseRedirect(reverse('App_main:buyer-home'))
    content = {
        'form': form,
    }

    return render(request, 'App_auth/profile_setup_view.html', context=content)


def freelancer_profile_view(request):
    profile = FreelancerProfileModel.objects.get(user=request.user)
    languages = LanguagesModel.objects.filter(user=request.user)
    skills = SkillListModel.objects.filter(user=request.user)
    categories = SkillCategoryModel.objects.all()

    add_language__form = LanguagesModelForm()
    add_skills__form = SkillListModelForm()
    total_money = TotalEarnModel.objects.filter(user=request.user)
    if total_money.exists():
        total_earned_by_user = total_money[0].total_money
    else:
        total_earned_by_user = 0
    content = {
        'profile': profile,
        'add_skills__form': add_skills__form,
        'add_language__form': add_language__form,
        'languages': languages,
        'skills': skills,
        'categories': categories,
        'total_earned_by_user': total_earned_by_user
    }

    return render(request, 'App_auth/freelancer_profile_view.html', context=content)


@login_required
def add_new_skill(request):
    if request.method == 'POST':
        form = SkillListModelForm(request.POST)
        if form.is_valid():
            thisForm = form.save(commit=False)
            thisForm.user = request.user
            thisForm.save()
            return HttpResponseRedirect(reverse('App_auth:freelancer-profile-view'))
    return HttpResponseRedirect(reverse('App_auth:freelancer-profile-view'))


@login_required
def add_new_language(request):
    if request.method == 'POST':
        form = LanguagesModelForm(request.POST)
        if form.is_valid():
            thisForm = form.save(commit=False)
            thisForm.user = request.user
            thisForm.save()
            return HttpResponseRedirect(reverse('App_auth:freelancer-profile-view'))
    return HttpResponseRedirect(reverse('App_auth:freelancer-profile-view'))


def buyer_profile_view(request):
    profile = BuyerProfileModel.objects.get(user=request.user)
    jobs = JobModel.objects.filter(author=request.user)
    content = {
        'profile': profile,
        'jobs': jobs,
    }
    return render(request, 'App_auth/buyer_profile_view.html', context=content)


# def buyer_profile_update(request):
#     if request.method == 'POST':
#         username = request.POST['username']
