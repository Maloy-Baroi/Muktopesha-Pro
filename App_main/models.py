from datetime import datetime
from distutils.command.upload import upload
from django.db import models
from App_auth.models import *
from django.contrib.auth.models import User


# Create your models here.
class JobCategoriesModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Category Name: {self.name}"


class SubCategoriesModel(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(JobCategoriesModel, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return f"SubCategory Name: {self.name}"


job_status = (
    ('Requested', 'Requested'),
    ('Pending', 'Pending'),
    ('Selected', 'Selected'),
    ('Running', 'Running'),
    ('Submitted', 'Submitted'),
    ('Completed', 'Completed')
)


class JobModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_post_author')
    job_title = models.CharField(max_length=500)
    company_name = models.CharField(max_length=500, blank=True, null=True)
    sub_category = models.ForeignKey(SubCategoriesModel, related_name='sub_categories', on_delete=models.DO_NOTHING)
    required_skills = models.CharField(max_length=800, blank=False)
    work_description = models.TextField()
    attachments = models.FileField(upload_to='job_attachments/', blank=True, null=True)
    stars_needed = models.CharField(max_length=100)
    validate_until = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default="Requested", choices=job_status)
    budget = models.IntegerField()


offerStatus = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
)


class OfferedToDoTheJobModel(models.Model):
    job = models.ForeignKey(JobModel, related_name='offered_do_the_job', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applicant')
    offer_text = models.TextField(max_length=200, blank=True, null=True)
    offer_status = models.CharField(max_length=100, default="Pending", choices=offerStatus)
    offer_sended_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class TotalEarnModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='total_earned')
    total_money = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user} total earned: ${self.total_money}"


class ChatRoom(models.Model):
    users = models.ManyToManyField(User, related_name='chat_room_users')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class MessageModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.CharField(max_length=10000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.DO_NOTHING)



class ProductSubmissionModel(models.Model):
    job = models.ForeignKey(JobModel, on_delete=models.CASCADE, related_name='job', related_query_name='job_product')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    drive_link = models.CharField(max_length=255, blank=True, null=True)
    files = models.FileField(upload_to="submitted_file", blank=True, null=True)


class FeeedbackModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feeedback_user')
    from_job = models.ForeignKey(JobModel, on_delete=models.CASCADE, related_name='feeedback_from_job')
    feedback_text = models.TextField()


