# Generated by Django 4.1.7 on 2024-11-22 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_alter_customuser_managers_customuser_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='name',
        ),
    ]