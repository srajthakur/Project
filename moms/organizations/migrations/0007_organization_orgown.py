# Generated by Django 5.1.3 on 2024-11-23 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0006_alter_customuser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='orgown',
            field=models.CharField(default='saksham', max_length=20),
            preserve_default=False,
        ),
    ]
