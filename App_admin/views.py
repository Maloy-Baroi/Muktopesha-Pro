from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test

from App_auth.forms import *
from App_auth.models import *
from App_main.forms import *
from App_main.models import *


# Create your views here.
def is_admin(user):
    return user.groups.filter(name='Admin').exists()


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_freelancer = FreelancerProfileModel.objects.all()
    total_buyer = BuyerProfileModel.objects.all()
    total_groups = Group.objects.all()
    all_user = User.objects.all()
    total_order = JobModel.objects.all()
    total_category = JobCategoriesModel.objects.all()
    total_sub_category = SubCategoriesModel.objects.all()
    content = {
        'total_freelancer': total_freelancer,
        'total_buyer': total_buyer,
        'total_groups': total_groups,
        'all_user': all_user,
        'total_order': total_order,
        'total_category': total_category,
        'total_sub_category': total_sub_category,
    }
    return render(request, 'App_admin/dashboard.html', context=content)


def admin_login_system(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if is_admin(user):
                return HttpResponseRedirect(reverse('App_admin:admin-dashboard'))
            return HttpResponseRedirect(reverse('App_admin:admin-login-system'))

    return render(request, 'App_admin/login_page.html')

@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def allUsers(request):
    users = User.objects.filter(is_superuser=False)
    content = {
        'users': users
    }
    return render(request, 'App_admin/all_users.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def delete_user(request, delete_id):
    user = User.objects.get(id=delete_id)
    user.delete()
    return HttpResponseRedirect(reverse('App_admin:all-users'))


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def freelancerProfile(request):
    profiles = FreelancerProfileModel.objects.filter()
    users = User.objects.filter(is_superuser=False)
    content = {
        'profiles': profiles,
        'users': users,
    }
    return render(request, 'App_admin/freelancer_profile.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def buyerProfile(request):
    profiles = BuyerProfileModel.objects.filter()
    users = User.objects.filter(is_superuser=False)
    content = {
        'profiles': profiles,
        'users': users,
    }
    return render(request, 'App_admin/buyer_profile.html', context=content)



@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def job_category(request):
    all_categories = JobCategoriesModel.objects.all()
    form = JobCategoriesModelForm()
    content = {
        'all_categories': all_categories,
        'form': form,
    }

    return render(request, 'App_admin/job_category_by_admin.html', context=content)



@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def add_job_category(request):
    if request.method == 'POST':
        form = JobCategoriesModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('App_admin:job-category'))


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def sub_category(request):
    all_sub_categories = SubCategoriesModel.objects.all()
    form = SubCategoriesModelForm()
    content = {
        'all_sub_categories': all_sub_categories,
        'form': form,
    }

    return render(request, 'App_admin/sub_category_by_admin.html', context=content)



@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def add_sub_category(request):
    if request.method == 'POST':
        form = SubCategoriesModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('App_admin:job-category'))



@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def all_jobs_view(request):
    all_jobs = JobModel.objects.all()
    content = {
        'all_jobs': all_jobs,
    }

    return render(request, 'App_admin/all_jobs_by_admin.html', context=content)


def job_offer_view(request):
    all_job_offers = OfferedToDoTheJobModel.objects.all()
    content = {
        'all_job_offers': all_job_offers,
    }
    return render(request, 'App_admin/offer_view.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def admin_group_view(request):
    groups = Group.objects.all()
    content = {
        'groups': groups
    }
    return render(request, 'App_admin/admin_groups.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def admin_group_add_view(request):
    if request.method == 'POST':
        name = request.POST.get('group_name')
        group = Group.objects.create(name=name)
        group.save()
        return HttpResponseRedirect(reverse('App_admin:admin-group-view'))


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def admin_group_delete_view(request, name):
    group = Group.objects.get(name=name)
    group.delete()
    return HttpResponseRedirect(reverse('App_admin:admin-group-view'))


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def all_chat_room_view(request):
    all_chat_room = ChatRoom.objects.all()
    content = {
        'chatRooms': all_chat_room
    }
    return render(request, 'App_admin/all_chat_room.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def admin_see_messages(request, pk):
    room = ChatRoom.objects.get(id=pk)
    messages = MessageModel.objects.filter(room=room)
    l = request.user.groups.values_list('name', flat=True)  # QuerySet Object
    l_as_list = list(l)
    content = {
        'messages': messages,
        'room': room,
    }
    return render(request, 'App_admin/all_messages.html', context=content)


def admin_get_messages(request, room):
    roomDetails = ChatRoom.objects.get(id=room)
    messages = MessageModel.objects.filter(room=room)
    listMessages = []
    for i in messages.values():
        user = User.objects.get(id=i['user_id'])
        i['userID'] = user.id
        i['username'] = user.username
        x_date = str(i['date'])[:16]
        i['date'] = x_date
        listMessages.append(i)
    return JsonResponse({"messages": listMessages})


# @login_required(login_url='App_admin:admin-login-system')
# @user_passes_test(is_admin)
# def admin_booking_view(request):
#     bookings = BookingModel.objects.all()
#     content = {
#         'bookings': bookings
#     }
#     return render(request, 'App_admin/admin_booking_view.html', context=content)


# @login_required(login_url='App_admin:admin-login-system')
# @user_passes_test(is_admin)
# def update_booking_status(request):
#     if request.method == 'POST':
#         bookingID = request.POST.get('bookingID')
#         bookingStatus = request.POST.get('status')
#         booking = BookingModel.objects.get(id=bookingID)
#         booking.status = bookingStatus
#         booking.save()
#         return HttpResponseRedirect(reverse('App_admin:admin-booking-view'))
#     return HttpResponseRedirect(reverse('App_admin:admin-booking-view'))


# @login_required(login_url='App_admin:admin-login-system')
# @user_passes_test(is_admin)
# def admin_campaign_view(request):
#     campaigns = CampaignModel.objects.all()
#     add_campaignForm = CampaignModelForm()
#     if request.method == 'POST':
#         add_campaignForm = CampaignModelForm(data=request.POST)
#         if add_campaignForm.is_valid():
#             add_campaignForm.save()
#     content = {
#         'campaigns': campaigns,
#         'campForm': add_campaignForm
#     }
#     return render(request, 'App_admin/admin_campaign_view.html', context=content)


# @login_required(login_url='App_admin:admin-login-system')
# @user_passes_test(is_admin)
# def admin_comment_view(request):
#     comments = CommentOnCampaign.objects.all()
#     content = {
#         'comments': comments
#     }
#     return render(request, 'App_admin/admin_comment_view.html', context=content)


# @login_required(login_url='App_admin:admin-login-system')
# @user_passes_test(is_admin)
# def admin_service_view(request):
#     services = ServicesModel.objects.all()
#     serviceForm = ServicesModelForm()
#     if request.method == 'POST':
#         details = request.POST.get('my-service-content')
#         serviceForm = ServicesModelForm(request.POST, request.FILES)
#         if serviceForm.is_valid():
#             serv = serviceForm.save(commit=False)
#             serv.details = details
#             serv.save()
#             return HttpResponseRedirect(reverse('App_admin:admin-service-view'))
#     content = {
#         'services': services,
#         'serviceForm': serviceForm,
#     }
#     return render(request, 'App_admin/admin_service_view.html', context=content)


# @login_required(login_url='App_admin:admin-login-system')
# @user_passes_test(is_admin)
# def admin_service_update_view(request, pk):
#     serv = ServicesModel.objects.get(id=pk)
#     form = ServicesUpdateModelForm(instance=serv)
#     if request.method == 'POST':
#         details = request.POST.get('my-service-content')
#         form = ServicesUpdateModelForm(request.POST, request.FILES, instance=serv)
#         if form.is_valid():
#             # form.save()
#             servForm = form.save(commit=False)
#             servForm.details = details
#             servForm.save()
#             return HttpResponseRedirect(reverse('App_admin:admin-service-view'))
#     content = {
#         'form': form,
#         'service': serv,
#     }
#     return render(request, 'App_admin/admin-service-update-view.html', context=content)


# @login_required(login_url='App_admin:admin-login-system')
# @user_passes_test(is_admin)
# def admin_service_update_status_view(request):
#     if request.method == 'POST':
#         status = request.POST.get('status')
#         servID = request.POST.get('serviceID')
#         service = ServicesModel.objects.get(id=servID)
#         service.status = status
#         service.save()
#         return HttpResponseRedirect(reverse('App_admin:admin-service-view'))


# @login_required(login_url='App_admin:admin-login-system')
# @user_passes_test(is_admin)
# def admin_gallery_view(request):
#     gallery = GalleryModel.objects.all()
#     galleryForm = GalleryModelForm()
#     if request.method == 'POST':
#         galleryForm = GalleryModelForm(request.POST, request.FILES)
#         if galleryForm.is_valid():
#             galleryForm.save()
#     content = {
#         'galleryImages': gallery,
#         'galleryForm': galleryForm,
#     }
#     return render(request, 'App_admin/admin_gallery_view.html', context=content)


# @login_required(login_url='App_admin:admin-login-system')
# @user_passes_test(is_admin)
# def admin_galleryImage_delete_view(request, deleteID):
#     image = GalleryModel.objects.get(id=deleteID)
#     image.delete()
#     return HttpResponseRedirect(reverse('App_admin:admin-gallery-view'))


# @login_required(login_url='App_admin:admin-login-system')
# @user_passes_test(is_admin)
# def admin_group_view(request):
#     groups = Group.objects.all()
#     content = {
#         'groups': groups
#     }
#     return render(request, 'App_admin/admin_groups.html', context=content)


# @login_required(login_url='App_admin:admin-login-system')
# @user_passes_test(is_admin)
# def admin_group_add_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('group_name')
#         group = Group.objects.create(name=name)
#         group.save()
#         return HttpResponseRedirect(reverse('App_admin:admin-group-view'))


# @login_required(login_url='App_admin:admin-login-system')
# @user_passes_test(is_admin)
# def admin_chat_room(request):
#     all_chat_room = ChatRoom.objects.all()
#     content = {
#         'chatRooms': all_chat_room
#     }
#     return render(request, 'App_admin/all_chat_room.html', context=content)


