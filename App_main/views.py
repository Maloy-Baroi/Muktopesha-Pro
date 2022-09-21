from email.policy import HTTP
import json
from urllib.request import HTTPRedirectHandler
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from App_auth.views import *
from App_auth.forms import *
from App_main.forms import *
from App_main.models import *
from datetime import date
from aamarpay.aamarpay import aamarPay


today = date.today()
today_month = today.month
today_year = today.year
today_day = today.day

# Create your views here.
@login_required
def freelancer_home_view(request):
    if is_freelancer(request.user):
        if is_profile_filled(request.user):
            skill_categories = SkillCategoryModel.objects.all()
            profile = FreelancerProfileModel.objects.get(user=request.user)
            best_freelancer = FreelancerProfileModel.objects.filter(stars=1)[:20]
            content = {
                'profile': profile,
                'skill_categories': skill_categories,
                'best_freelancer': best_freelancer,
            }
            return render(request, 'App_main/Freelancer/freelancer_home.html', context=content)
        else:
            return HttpResponseRedirect(reverse('App_auth:profile-setup-view'))
    else:
        return redirect('/buyer')


@login_required
@user_passes_test(is_freelancer)
def find_all_jobs(request):
    jobs = JobModel.objects.filter(status='Pending')
    jobList = []
    for job in jobs:
        if today_day >= job.validate_until.day and today_month >= job.validate_until.month and today_year >= job.validate_until.year:
            if OfferedToDoTheJobModel.objects.filter(user=request.user, job=job).exists():
                pass
            else:    
                jobList.append(job)
    mySkills = SkillListModel.objects.filter(user=request.user)
    mySkillsCategories = set([x.category.categoryName for x in mySkills])
    myJobs = []
    for job in jobs:
        if job.sub_category.category.name in mySkillsCategories:
            myJobs.append(job)
    
    all_my_offer = OfferedToDoTheJobModel.objects.filter(user=request.user)
    all_my_offer_I_sent = [x.job for x in all_my_offer]
    content = {
        'jobList': jobs,
        'jobs': myJobs,
        'all_my_offer_I_sent': all_my_offer_I_sent,
    }
    return render(request, 'App_main/freelancer/find_all_jobs.html', context=content)


@login_required
@user_passes_test(is_freelancer)
def apply_job(request, id):
    job = JobModel.objects.get(id=id)
    if request.method == 'POST':
        extra_text = request.POST.get('offer-text')
        offer = OfferedToDoTheJobModel(job=job, user=request.user, offer_text=extra_text)
        offer.save()
        return HttpResponseRedirect(reverse('App_main:find-all-jobs'))
    return render(request, "jobs/job_apply.html")


@login_required
@user_passes_test(is_freelancer)
def all_freelancer_view(request):
    freelancers = FreelancerProfileModel.objects.all()
    content = {
        'freelancers': freelancers,
    }
    return render(request, 'App_main/Freelancer/all_freelancer.html', context=content)


@login_required
@user_passes_test(is_freelancer)
def all_you_applied_as_freelancer(request):
    offers = OfferedToDoTheJobModel.objects.filter(user=request.user)
    content = {
        'offfers': offers,
    }
    return render(request, 'App_main/Freelancer/all_applied.html', context=content)



def product_submission(request, jobID):
    form = ProductSubmissionModelForm()
    if request.method == 'POST':
        job = JobModel.objects.get(id=jobID)
        form = ProductSubmissionModelForm(request.POST, request.FILES)
        if form.is_valid():
            thisForm = form.save(commit=False)
            thisForm.sender = request.user
            thisForm.receiver = job.author
            thisForm.job = job
            job.status = 'Submitted'
            job.save()
            thisForm.save()
            return HttpResponseRedirect(reverse('App_main:freelancer-home'))
    content = {
        'form': form,
    }
    return render(request, 'App_main/Freelancer/product_submission.html', context=content)




@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_freelancer)
def freelancer_chat_room(request):
    all_chat_room = ChatRoom.objects.all()
    my_chat_room = []

    for room in all_chat_room:
        if request.user in room.users.all():
            my_chat_room.append(room)
        
    profile = BuyerProfileModel.objects.filter(user=request.user)
    content = {
        'myChatRooms': my_chat_room,
        'buyer': profile,
    }
    return render(request, 'App_main/Buyer/buyer_all_chat_room.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_freelancer)
def freelancer_single_chat_room(request, roomID):
    room = ChatRoom.objects.get(id=roomID)
    users = room.users.all()
    content = {
        'room': room,
    }
    return render(request, 'App_main/Freelancer/freelancer_single_chatroom_chat.html', context=content)


def freelancer_get_messages(request, roomID):
    roomDetails = ChatRoom.objects.get(id=roomID)
    messages = MessageModel.objects.filter(room=roomID)
    print(messages)
    listMessages = []
    for i in messages.values():
        user = User.objects.get(id=i['user_id'])
        i['userID'] = user.id
        i['username'] = user.username
        x_date = str(i['date'])[:16]
        i['date'] = x_date
        listMessages.append(i)
    return JsonResponse({"messages": listMessages})


def freelacer_message_send(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        roomID = request.POST.get('room_id')
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        thisRoom = ChatRoom.objects.get(name=roomID)
        newMessage = MessageModel.objects.create(value=message, user=user, room=thisRoom)
        newMessage.save()
        return HttpResponse("Message Send Successfully")


def freelancer_message_send(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        roomID = request.POST.get('room_id')
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        thisRoom = ChatRoom.objects.get(name=roomID)
        newMessage = MessageModel.objects.create(value=message, user=user, room=thisRoom)
        newMessage.save()
        return HttpResponse("Message Send Successfully")

# End Freelancer Part

# Buyer Part
@login_required
def buyer_home_view(request):
    if is_buyer(request.user):
        if is_profile_filled(request.user):
            skill_categories = SkillCategoryModel.objects.all()
            best_freelancer = FreelancerProfileModel.objects.filter(stars=1)[:20]
            content = {
                'skill_categories': skill_categories,
                'best_freelancer': best_freelancer,
            }
            return render(request, 'App_main/Buyer/buyer_home.html', context=content)
        else:
            return HttpResponseRedirect(reverse('App_auth:profile-setup-view'))
    else:
        return redirect('/')
        

def aamarPay_view(request):
    # pay = aamarPay(isSandbox=True,transactionAmount=600)
    # paymentpath = pay.payment()
    # return redirect(paymentpath)
    return render(request, 'App_main/Buyer/aamarPay.html')


def buyer_job_post(request):
    form = JobModelForm()
    newBudget = 0
    if request.method == 'POST':
        form = JobModelForm(request.POST, request.FILES)
        if form.is_valid():
            thisForm = form.save(commit=False)
            budget = form.cleaned_data.get('budget')
            if budget%5 == 0:
                newBudget = budget
            elif budget%5 <= 2:
                r = budget//5
                newBudget = r*5
            elif budget%5 >= 3:
                r= budget // 5
                newBudget = (r+1)*5
            thisForm.author = request.user
            thisForm.status = "Requested"
            thisForm.budget = newBudget
            thisForm.save()
            return HttpResponseRedirect(reverse('App_main:aamarPay-view'))
    
    content = {
        'form': form,
    }
    return render(request, 'App_main/Buyer/buyer_job_post_view.html', context=content)


@login_required
@user_passes_test(is_buyer)
def buyer_finds_freelancer(request):
    freelancers = FreelancerProfileModel.objects.all()
    content = {
        'freelancers': freelancers,
    }
    return render(request, 'App_main/Buyer/buyer_finds_freelancer.html', context=content)


@login_required
@user_passes_test(is_buyer)
def single_vision_of_job_by_buyer(request, id):
    job = JobModel.objects.get(id=id)
    offers = OfferedToDoTheJobModel.objects.filter(job=job)
    content = {
        'job': job,
        'offers': offers,
    }

    return render(request, 'App_main/Buyer/everything_in_single_job.html', context=content)


@login_required
@user_passes_test(is_buyer)
def see_freelancer_profiles(request, id, jobID):
    user = User.objects.get(id=id)
    profile = FreelancerProfileModel.objects.get(user=user)
    languages = LanguagesModel.objects.filter(user=profile.user)
    skills = SkillListModel.objects.filter(user=profile.user)
    content = {
        'profile': profile,
        'languages': languages,
        'skills': skills,
        'job_id': jobID,
    }
    return render(request, 'App_main/Buyer/view_freelancer.html', context=content)


@login_required
@user_passes_test(is_buyer)
def offer_accepted_by_buyer(request, offer_id, job_id):
    offer = OfferedToDoTheJobModel.objects.get(id=offer_id)
    job = JobModel.objects.get(id=job_id)
    offer.offer_status = 'Approved'
    job.status = 'Selected'
    offer.save()
    job.save()
    return HttpResponseRedirect(reverse('App_auth:buyer-profile-view'))


@login_required
@user_passes_test(is_buyer)
def first_message_from_buyer_to_sender(request, profileID, jobID):
    job = JobModel.objects.get(id=jobID)
    buyer_profile = BuyerProfileModel.objects.get(user=request.user)
    freelancer_profile = FreelancerProfileModel.objects.get(id=profileID)
    all_chat_room = ChatRoom.objects.all()
    room = ChatRoom.objects.get_or_create(name=f"Buyer:{buyer_profile.full_name}-Seller:{freelancer_profile.full_name}")[0]
    room.users.add(request.user)
    room.users.add(freelancer_profile.user)
    theMessage = f"I am {buyer_profile.full_name}, You sended an offer to work for me on {job.job_title}. I would like to talk about it."
    message = MessageModel(user=request.user, value=theMessage, room=room)
    message.save()
    # return HttpResponseRedirect(reverse(''))
    return HttpResponseRedirect(reverse('App_main:buyer-chat-rooms'))



@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_buyer)
def buyer_chat_room(request):
    all_chat_room = ChatRoom.objects.all()
    my_chat_room = []

    for room in all_chat_room:
        if request.user in room.users.all():
            my_chat_room.append(room)
        
    profile = BuyerProfileModel.objects.filter(user=request.user)
    content = {
        'myChatRooms': my_chat_room,
        'buyer': profile,
    }
    return render(request, 'App_main/Buyer/buyer_all_chat_room.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_buyer)
def buyer_single_chat_room(request, roomID):
    room = ChatRoom.objects.get(id=roomID)
    users = room.users.all()
    content = {
        'room': room,
    }
    return render(request, 'App_main/Buyer/buyer_single_chatroom_chat.html', context=content)


def buyer_get_messages(request, roomID):
    roomDetails = ChatRoom.objects.get(id=roomID)
    messages = MessageModel.objects.filter(room=roomID)
    print(messages)
    listMessages = []
    for i in messages.values():
        user = User.objects.get(id=i['user_id'])
        i['userID'] = user.id
        i['username'] = user.username
        x_date = str(i['date'])[:16]
        i['date'] = x_date
        listMessages.append(i)
    return JsonResponse({"messages": listMessages})


def buyer_message_send(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        roomID = request.POST.get('room_id')
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        thisRoom = ChatRoom.objects.get(name=roomID)
        newMessage = MessageModel.objects.create(value=message, user=user, room=thisRoom)
        newMessage.save()
        return HttpResponse("Message Send Successfully")


def buyer_reviewing_submitted_product(request, jobID):
    job = JobModel.objects.get(id=jobID)
    submitted_product = ProductSubmissionModel.objects.filter(job=job)
    profile = FreelancerProfileModel.objects.get(user=submitted_product[0].sender)
    content = {
        'job': job,
        'submitted_product': submitted_product[0],
        'profile': profile,
    }
    return render(request, 'App_main/Buyer/buyer_reviewing_submitted_product.html', context=content)


def buyer_accepts_the_product(request):
    if request.method == 'POST':
        feed_back = request.POST.get('feedback')
        star = request.POST.get('star')
        jobID = request.POST.get('jobID')
        profileID = request.POST.get('profileID')
        profile = FreelancerProfileModel.objects.get(id=profileID)
        job = JobModel.objects.get(id=jobID)
        job.status = "Completed"
        job.save()
        total_star = (int(profile.stars) + int(star))/2;
        profile.stars = total_star
        profile.save()
        profileUser = profile.user
        user = User.objects.get(id=profileUser.id)
        feedMe = FeeedbackModel.objects.create(user=user, from_job=job, feedback_text=feed_back)
        feedMe.save()
        total_money = job.budget * 0.8
        total_earned_by_user = TotalEarnModel.objects.get_or_create(user=user)[0]
        total_earned_by_user.total_money += total_money
        print(total_earned_by_user.total_money)
        total_earned_by_user.save()
        return HttpResponseRedirect(reverse('App_main:buyer-reviewing-submitted-product', kwargs=({'jobID': job.id})))

        

