# Generated by Django 3.0.12 on 2021-02-21 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='icon',
            field=models.ImageField(blank=True, default='', null=True, upload_to='profile/'),
        ),
    ]
