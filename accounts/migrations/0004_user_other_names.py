# Generated by Django 4.1 on 2022-08-08 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_school_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='other_names',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
