from email.policy import default
from hashlib import blake2b
from django.db import models

# Extra Dependencies
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy

# Create your models here.
phone_regex = RegexValidator(regex=r"^\+?(88)01[3-9][0-9]{8}$",
                             message=gettext_lazy('Enter Bangladeshi Number with country code'))


class SkillCategoryModel(models.Model):
    categoryName = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="category_logo/", blank=True)

    def __str__(self):
        return f"{self.categoryName}"


SKILL_LEVELS = (
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Expart', 'Expart'),
)


class SkillListModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_skill_list')
    title = models.CharField(max_length=100)
    category = models.ForeignKey(SkillCategoryModel, on_delete=models.DO_NOTHING, blank=True)
    skill_level = models.CharField(max_length=100, null=True, blank=True, choices=SKILL_LEVELS)

    def __str__(self):
        return f"skill --> {self.title}"


class EducationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_education')
    level_of_education = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    institution = models.CharField(max_length=200)

    def __str__(self):
        return self.level_of_education


class Extra_curricular_Activities_Model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_extra_curricular')
    topic = models.CharField(max_length=254)
    perform_time = models.DateField(default='2000-01-01')

    def __str__(self):
        return self.topic


class Co_curricular_Activities_Model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_co_curricular')
    topic = models.CharField(max_length=254)
    perform_time = models.DateField(default='2000-01-01')

    def __str__(self):
        return self.topic


class AchievementModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_achievements')
    topic = models.CharField(max_length=254)
    perform_time = models.DateField(default='2000-01-01')


class ExperiencesModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_experiences')
    position = models.CharField(max_length=100)
    starting_year = models.DateField(default='2000-01-01')
    leaving_year = models.DateField(default='2000-01-01', blank=True, null=True)
    location = models.CharField(max_length=200)
    Company = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.user}'s experiences on {self.Company} as a/an {self.position}"


LANGUAGE_LEVELS = (
    ('Beginner', 'Beginner'),
    ('Good For work', 'Good For work'),
    ('Native', 'Native'),
)


class LanguagesModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_languages')
    laguage_name = models.CharField(max_length=100)
    language_level = models.CharField(max_length=100, choices=LANGUAGE_LEVELS)

    def __str__(self):
        return f"{self.user}'s language {self.laguage_name}"


sex = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)


class FreelancerProfileModel(models.Model):
    user = models.ForeignKey(User, related_name='freelancer_profile', related_query_name="freelancer_profile", on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='Freelancer_cover_image')
    profile_picture = models.ImageField(upload_to='freelancer_profile_picture/')
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(validators=[phone_regex], max_length=14)
    Bkash_number = models.CharField(validators=[phone_regex], max_length=14)
    address = models.CharField(max_length=50)
    what_you_are = models.CharField(max_length=100)
    member_since = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)
    Date_of_Birth = models.DateField(default='2000-01-01')
    gender = models.CharField(choices=sex, max_length=10)
    stars = models.IntegerField(default=0)
    activity_status = models.BooleanField(default=False)



class BuyerProfileModel(models.Model):
    user = models.ForeignKey(User, related_name='buyer_profile', on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='buyer_profile_picture/')
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=14)
    address = models.CharField(max_length=50)
    status = models.CharField(max_length=100)
    member_since = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)
    Date_of_Birth = models.DateField(default='2000-01-01')
    gender = models.CharField(choices=sex, max_length=10)
    country = models.CharField(max_length=100, default='Bangladesh')
