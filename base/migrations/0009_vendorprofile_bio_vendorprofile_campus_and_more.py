# Generated by Django 4.2.7 on 2024-03-27 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_vendorprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorprofile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vendorprofile',
            name='campus',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='vendorprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
