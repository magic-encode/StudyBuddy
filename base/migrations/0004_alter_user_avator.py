# Generated by Django 4.1.5 on 2023-01-27 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_user_avator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avator',
            field=models.ImageField(default='avatar.svg', null=True, upload_to='media/'),
        ),
    ]
