# Generated by Django 2.0.2 on 2018-03-09 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20180309_1415'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='user',
        ),
        migrations.RemoveField(
            model_name='memberaddress',
            name='district',
        ),
        migrations.RemoveField(
            model_name='memberaddress',
            name='member',
        ),
        migrations.DeleteModel(
            name='Member',
        ),
        migrations.DeleteModel(
            name='MemberAddress',
        ),
    ]
