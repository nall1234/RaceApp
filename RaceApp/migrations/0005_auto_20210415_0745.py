# Generated by Django 2.2 on 2021-04-15 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RaceApp', '0004_auto_20210415_0742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='images/blank.jpg', null=True, upload_to='images/'),
        ),
    ]
