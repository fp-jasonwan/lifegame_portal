# Generated by Django 3.1.2 on 2021-03-08 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_user_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
