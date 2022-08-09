# Generated by Django 4.1 on 2022-08-09 13:15

import accounts.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='school_id',
            field=models.CharField(default=accounts.utils.generate_school_id, editable=False, max_length=100, unique=True),
        ),
    ]
