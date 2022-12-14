# Generated by Django 4.0.4 on 2022-09-21 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_main', '0020_feeedbackmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobmodel',
            name='status',
            field=models.CharField(choices=[('Requested', 'Requested'), ('Pending', 'Pending'), ('Selected', 'Selected'), ('Running', 'Running'), ('Submitted', 'Submitted'), ('Completed', 'Completed')], default='Requested', max_length=100),
        ),
        migrations.AlterField(
            model_name='productsubmissionmodel',
            name='drive_link',
            field=models.CharField(default='None', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productsubmissionmodel',
            name='files',
            field=models.FileField(default=None, upload_to='submitted_file'),
            preserve_default=False,
        ),
    ]
