# Generated by Django 4.0.4 on 2022-09-20 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_auth', '0008_alter_buyerprofilemodel_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyerprofilemodel',
            name='phone_number',
            field=models.CharField(max_length=14),
        ),
    ]