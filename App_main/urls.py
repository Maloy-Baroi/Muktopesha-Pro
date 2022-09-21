from django.urls import path
from App_main.views import *

app_name = 'App_main'

urlpatterns = [
    # Freelancer App_main
    path('', freelancer_home_view, name='freelancer-home'),
    path('find-all-jobs/', find_all_jobs, name='find-all-jobs'),
    path('apply-job/<int:id>/', apply_job, name='apply-job'),
    path('all-freelancer-view/', all_freelancer_view, name='all-freelancer-view'),
    path('all-you_applied-as-freelancer/', all_you_applied_as_freelancer, 
        name='all-you-applied-as-freelancer'),
    path('product-submission/<int:jobID>/', product_submission, name='product-submission'),



    # Buyer App_main
    path('buyer/', buyer_home_view, name='buyer-home'),
    path('buyer-job-post/', buyer_job_post, name='buyer-job-post'),
    path('aamarPayview', aamarPay_view,name='aamarPay-view'),
    path('buyer-finds-freelancer/', buyer_finds_freelancer, name='buyer-finds-freelancer'),
    path('single-vision-of-job-by-buyer/<int:id>/', single_vision_of_job_by_buyer, 
        name='single-vision-of-job-by-buyer'),
    path('freelancer-profile-view-by-buyer/<int:id>/<int:jobID>/', see_freelancer_profiles,
        name='freelancer-profile-view-by-buyer'),
    
    path('freelancer-chat-rooms/', freelancer_chat_room,name='freelancer-chat-rooms'),
    # offer_id, job_id
    path('freelancer-single-chat-room/<int:roomID>/', freelancer_single_chat_room, name='freelancer-single-chat-room'),

    path('freelancer-getMessages/<int:roomID>/', buyer_get_messages, name='get-messages'),
    path('freelancer-send-message/', freelacer_message_send, name='freelancer-send-message'),


    path('first-message-from-buyer-to-sender/<int:profileID>/<int:jobID>/', 
        first_message_from_buyer_to_sender, 
        name='first-message-from-buyer-to-sender'),
    path('buyer-chat-rooms/', buyer_chat_room,name='buyer-chat-rooms'),
    # offer_id, job_id
    path('offer-accepted-by-buyer/<int:offer_id>/<int:job_id>/', offer_accepted_by_buyer,name='offer-accepted-by-buyer'),
    path('buyer-single-chat-room/<int:roomID>/', buyer_single_chat_room, name='buyer-single-chat-room'),

    path('buyer-getMessages/<int:roomID>/', buyer_get_messages, name='get-messages'),
    path('buyer-send-message/', buyer_message_send, name='buyer-send-message'),
    path('buyer-reviewing-submitted-product/<int:jobID>/', buyer_reviewing_submitted_product, 
        name='buyer-reviewing-submitted-product'),
    path('buyer-accepts-the-product', buyer_accepts_the_product, name='buyer-accepts-the-product'),
]

